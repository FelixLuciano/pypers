# import logging
# from datetime import datetime
# from pathlib import Path

from faulthandler import disable
import ipywidgets as widgets
from IPython.display import Image, display

import __main__

from .Google import Google
from .Preview_controls import Preview_controls


class Send_controls:
    __controls = None
    # __observers = []

    def init():
        Google.authenticate()

        if Send_controls.__controls == None:
            Send_controls.__update_controls()
            # Send_controls.__mount_listeners()

    @staticmethod
    def display():
        display(Send_controls.__controls)

    @staticmethod
    def __update_controls():
        user_picture = widgets.Output()
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
                widgets.HBox([Preview_controls.get_user_select()]),
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

        tabs = widgets.Tab([test_tab])

        tabs.set_title(0, "Send test")
        # tabs.set_title(1, "Dispatch")

        Send_controls.__controls = widgets.HBox(
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

        with user_picture:
            display(Image(url=Google.get_userinfo()["picture"]))

    # @staticmethod
    # def __mount_listeners():
    #     @__get_send_test_button().on_click
    #     def send_test(button):
    #         test_send_button.disabled = True
    #         test_send_button.button_style = "info"

    #         mail = Send.get_Mail(
    #             page=page.render(Preview.selected_user),
    #             sender=sender_select.value,
    #             to=test_destination_input.value,
    #             subject=subject_input.value,
    #         )

    #         Google.Gmail.send(mail)

    #         test_send_button.disabled = False
    #         test_send_button.button_style = "success"

    @staticmethod
    def __get_sender_select():
        return Send_controls.__controls.children[0].children[0].children[0]

    @staticmethod
    def __get_subject_input():
        return Send_controls.__controls.children[0].children[1].children[0]

    @staticmethod
    def __get_test_destination_input():
        return Send_controls.__controls.children[1].children[2].children[0].children[0].children[0]

    @staticmethod
    def __get_send_test_button():
        return Send_controls.__controls.children[1].children[2].children[0].children[1].children[1]

    # @staticmethod
    # def display(page):
    #     destination_select = widgets.SelectMultiple(
    #         options=mails,
    #         description="To:",
    #         rows=min(len(mails), 10),
    #         layout={"flex": "1 1 100%"},
    #     )

    #     send_button = widgets.Button(
    #         description=" Send all", button_style="warning", icon="rocket"
    #     )

    #     output = widgets.Output(layout={"flex": "1 1 100%"})

    #     send_tab = widgets.VBox(
    #         [
    #             widgets.HBox([destination_select]),
    #             widgets.HBox(
    #                 [
    #                     widgets.VBox(
    #                         layout={"width": "88px"},
    #                     ),
    #                     send_button,
    #                 ],
    #                 layout={"padding": "16px 0 16px 0"},
    #             ),
    #             output,
    #         ],
    #         layout={"width": "99%"},
    #     )

    #     @test_send_button.on_click
    #     def send_test(button):
    #         test_send_button.disabled = True
    #         test_send_button.button_style = "info"

    #         mail = Send.get_Mail(
    #             page=page.render(Preview.selected_user),
    #             sender=sender_select.value,
    #             to=test_destination_input.value,
    #             subject=subject_input.value,
    #         )

    #         Google.Gmail.send(mail)

    #         test_send_button.disabled = False
    #         test_send_button.button_style = "success"

    #     @send_button.on_click
    #     def send_all(button):
    #         send_button.disabled = True
    #         log_filename = Path(
    #             "logs", f'{datetime.now().strftime(f"%Y-%m-%d %H-%M-%S-%f")}.log'
    #         )
    #         logger = logging.getLogger(str(log_filename))
    #         template = page.get_template()

    #         log_filename.parent.mkdir(parents=True, exist_ok=True)
    #         logging.basicConfig(
    #             filename=str(log_filename),
    #             filemode="w",
    #             format="%(asctime)s.%(msecs)03d - %(message) s",
    #             datefmt="%Y-%m-%d %H-%M-%S",
    #             level=logging.INFO,
    #         )

    #         progress = widgets.IntProgress(
    #             description="Sending...",
    #             value=0,
    #             min=0,
    #             max=len(destination_select.value),
    #             step=1,
    #         )

    #         output.clear_output()

    #         with output:
    #             display(progress)

    #             try:
    #                 for username in destination_select.value:
    #                     user = users.loc[mails == username].iloc[0]
    #                     mail = Send.get_Mail(
    #                         page=template.render(**page.get_props(user)),
    #                         sender=sender_select.value,
    #                         to=user[users.email_column],
    #                         subject=subject_input.value,
    #                     )

    #                     Google.Gmail.send(mail)
    #                     logger.info(f"Successfully sent to {username}")

    #                     progress.value += 1

    #                 progress.description = "Success!"
    #                 progress.bar_style = "success"
    #             except Exception as error:
    #                 progress.bar_style = "danger"

    #                 logger.error(error)

    #                 raise error
    #             finally:
    #                 send_button.disabled = False

    #     return layout
