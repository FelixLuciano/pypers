import logging
from base64 import urlsafe_b64encode
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import ipywidgets as widgets
from IPython.display import Image, display

import __main__

from .Google import Google
from .Preview import Preview
from .Send import Send


class Send:
    @staticmethod
    def get_Mail(page, sender, to, subject):
        mail = MIMEMultipart()
        page_mime = MIMEText(page, "html")

        mail["to"] = to
        mail["from"] = sender
        mail["subject"] = subject

        mail.attach(page_mime)

        return {"raw": urlsafe_b64encode(mail.as_bytes()).decode()}

    @staticmethod
    def display(page):
        users = vars(__main__)["users"]

        if hasattr(users, "name_column"):
            if isinstance(users.name_column, str):
                mails = (
                    users[users.name_column] + " <" + users[users.email_column] + ">"
                )
            else:
                mails = (
                    users.loc[:, users.name_column].apply(" - ".join, 1)
                    + " <"
                    + users[users.email_column]
                    + ">"
                )
        else:
            mails = users[users.email_column]

        Google.authenticate()

        user_picture = widgets.Output()

        with user_picture:
            display(Image(url=Google.userinfo["picture"]))

        sender_select = widgets.Dropdown(
            description="Send as:",
            options=Google.Gmail.get_aliases(),
            layout={"flex": "1 1 100%"},
        )

        subject_input = widgets.Text(
            description="Subject:", layout={"flex": "1 1 100%"}
        )

        test_destination_input = widgets.Text(
            description="To:",
            placeholder="mail@example.com",
            layout={"flex": "1 1 100%"},
        )
        test_send_button = widgets.Button(
            description=" Send test", button_style="info", icon="paper-plane"
        )

        test_tab = widgets.VBox(
            [
                widgets.HBox([test_destination_input]),
                widgets.HBox(
                    [
                        widgets.VBox(
                            layout={"width": "88px"},
                        ),
                        test_send_button,
                    ],
                    layout={"padding": "16px 0 16px 0"},
                ),
            ]
        )

        destination_select = widgets.SelectMultiple(
            options=mails,
            description="To:",
            rows=min(len(mails), 10),
            layout={"flex": "1 1 100%"},
        )

        send_button = widgets.Button(
            description=" Send all", button_style="warning", icon="rocket"
        )

        output = widgets.Output(layout={"flex": "1 1 100%"})

        send_tab = widgets.VBox(
            [
                widgets.HBox([destination_select]),
                widgets.HBox(
                    [
                        widgets.VBox(
                            layout={"width": "88px"},
                        ),
                        send_button,
                    ],
                    layout={"padding": "16px 0 16px 0"},
                ),
                output,
            ],
            layout={"width": "99%"},
        )

        tabs = widgets.Tab([test_tab, send_tab])

        tabs.set_title(0, "Send test")
        tabs.set_title(1, "Dispatch")

        layout = widgets.HBox(
            [
                user_picture,
                widgets.VBox(
                    [
                        widgets.HBox([sender_select]),
                        widgets.HBox([subject_input]),
                        tabs,
                    ],
                    layout={"flex": "1 1 100%", "padding": "0 0 0 16px"},
                ),
            ]
        )

        @test_send_button.on_click
        def send_test(button):
            test_send_button.disabled = True
            test_send_button.button_style = "info"

            mail = Send.get_Mail(
                page=page.render(Preview.selected_user),
                sender=sender_select.value,
                to=test_destination_input.value,
                subject=subject_input.value,
            )

            Google.Gmail.send(mail)

            test_send_button.disabled = False
            test_send_button.button_style = "success"

        @send_button.on_click
        def send_all(button):
            send_button.disabled = True
            log_filename = Path(
                "logs", f'{datetime.now().strftime(f"%Y-%m-%d %H-%M-%S-%f")}.log'
            )
            logger = logging.getLogger(str(log_filename))
            template = page.get_template()

            log_filename.parent.mkdir(parents=True, exist_ok=True)
            logging.basicConfig(
                filename=str(log_filename),
                filemode="w",
                format="%(asctime)s.%(msecs)03d - %(message) s",
                datefmt="%Y-%m-%d %H-%M-%S",
                level=logging.INFO,
            )

            progress = widgets.IntProgress(
                description="Sending...",
                value=0,
                min=0,
                max=len(destination_select.value),
                step=1,
            )

            output.clear_output()

            with output:
                display(progress)

                try:
                    for username in destination_select.value:
                        user = users.loc[mails == username].iloc[0]
                        mail = Send.get_Mail(
                            page=template.render(**page.get_props(user)),
                            sender=sender_select.value,
                            to=user[users.email_column],
                            subject=subject_input.value,
                        )

                        Google.Gmail.send(mail)
                        logger.info(f"Successfully sent to {username}")

                        progress.value += 1

                    progress.description = "Success!"
                    progress.bar_style = "success"
                except Exception as error:
                    progress.bar_style = "danger"

                    logger.error(error)

                    raise error
                finally:
                    send_button.disabled = False

        return layout
