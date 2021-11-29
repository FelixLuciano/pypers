from base64 import urlsafe_b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import *


class Mail(MIMEMultipart):
    def __init__(self, page, user_props):
        MIMEMultipart.__init__(self)

        user_page = page.get_page(user_props)
        page_mime = MIMEText(user_page, "html")

        self["to"] = user_props["Email"]
        self["From"] = f"\"{page.meta['name']}\" <felixluciano.200@gmail.com>"
        self["subject"] = page.meta["subject"]

        self.attach(page_mime)


    def get_mail(self):
        return {
            "raw": urlsafe_b64encode(self.as_bytes()).decode()
        }
