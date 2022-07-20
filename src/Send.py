from base64 import urlsafe_b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import __main__
import ipywidgets as widgets

from .Google import Google
from .Preview import Preview


class Send:
    @staticmethod
    def get_Mail(page, user, name, to, subject):
        mail = MIMEMultipart()

        page = page.get_template().render(**page.get_props(user))
        page_mime = MIMEText(page, "html")

        mail['to'] = to
        mail['from'] = f"{name} <{Google.userinfo['email']}>"
        mail['subject'] = subject

        mail.attach(page_mime)

        return {
            'raw': urlsafe_b64encode(mail.as_bytes()).decode()
        }


    @staticmethod
    def display(page):
        users = vars(__main__)['users']

        if hasattr(users, 'name_column'):
            mails = users[users.name_column] + ' <' + users[users.mail_column] + '>'
        else:
            mails = users[users.mail_column]

        from_input = widgets.Text(
            description='From:',
            placeholder='mail@example.com',
            layout={
                'flex': '1 1 100%'
            }
        )

        subject_input = widgets.Text(
            description='Subject:',
            layout={
                'flex': '1 1 100%'
            }
        )

        test_destination_input = widgets.Text(
            description='To:',
            placeholder='mail@example.com',
            layout={
                'flex': '1 1 100%'
            }
        )
        test_send_button = widgets.Button(
            description=' Send',
            button_style="info",
            icon='paper-plane'
        )

        test_tab = widgets.HBox([
            test_destination_input,
            test_send_button
        ])

        destination_select = widgets.SelectMultiple(
            options=mails,
            description='To:',
            rows=min(len(mails), 10),
            layout={
                'flex': '1 1 100%'
            }
        )

        program_picker = widgets.DatePicker(
            description=' Program',
            layout={
                'flex': '1 1 100%'
            }
        )

        send_button = widgets.Button(
            description=' Send',
            button_style="warning",
            icon='rocket'
        )

        send_tab = widgets.VBox([
            widgets.HBox([
                destination_select
            ]),
            widgets.HBox([
                program_picker,
                send_button
            ])
        ],
        layout= {
            'width': '99%'
        })

        tabs = widgets.Tab([
            test_tab,
            send_tab
        ])

        tabs.set_title(0, 'Send test')
        tabs.set_title(1, 'Dispatch')

        layout = widgets.VBox([
            widgets.HBox([
                from_input
            ]),
            widgets.HBox([
                subject_input
            ]),
            tabs
        ])

        def send_test(button):
            test_send_button.disabled = True

            Google.authenticate()

            mail = Send.get_Mail(
                page=page,
                user=Preview.selected_user,
                name=from_input.value,
                to=test_destination_input.value,
                subject=subject_input.value
            )

            Google.Gmail.send(mail)
            
            test_send_button.disabled = False
        
        test_send_button.on_click(send_test)

        return layout
