import random
import string
from datetime import datetime

from lib.config import *
from lib.lists import MAILING_LIST
from lib.mail import Mail
from lib.page import Page
from lib.services import GMAIL_SERVICE


def dispatch_messages(quiet=False):
    page = Page()
    size = len(MAILING_LIST)
    index = 1

    with GMAIL_SERVICE as service:
        for user in MAILING_LIST:
            message = Mail(page, user)
            response = service.users().messages().send(userId="me", body=message.get_mail()).execute()

            if not quiet:
                print(f"Sending {index} of {size}...")

            index += 1


def confirm_prompt(prompt):
    confirm = input(f"{prompt} (yes/no) ").lower()

    return confirm in ("y", "yes")


def send():
    if confirm_prompt("Send?"):
        if IS_TEST:
            dispatch_messages(quiet=True)
            print("Test launched successfully!")
        else:
            code = ''.join(random.choice(string.ascii_letters) for _ in range(CAPTHCA_CODE_RANGE))
            typed = input(f"Type \"{code}\": ")

            if not typed == code:
                print("Invalid code!")
            else:
                dispatch_messages()
                print("Newsletter launched successfully!")


if __name__ == "__main__":
    send()
