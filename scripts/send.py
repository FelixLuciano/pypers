import os
import re
from base64 import urlsafe_b64encode
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from build import build_feed, build_test, get_config


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]


def atuth(scopes):
    credentials = None
    if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json', scopes)

    if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
            else:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
                    credentials = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                    token.write(credentials.to_json())

    return credentials


def get_table(values):
    header = [h.replace(" ", "_") for h in values["values"][0]]
    body = values["values"][1:]

    return [dict(zip(header, row)) for row in body]


def fetch_subscribers_data(credentials, config):
    sheet_id = config["sheet"]["id"]
    pages = config["sheet"]["pages"]

    with build("sheets", "v4", credentials=credentials) as service:
        sheets = service.spreadsheets().values()

        subs_sheet  = sheets.get(spreadsheetId=sheet_id, range=pages["subscribers"]).execute()
        unsub_sheet = sheets.get(spreadsheetId=sheet_id, range=pages["unsibscribers"]).execute()

    subs = get_table(subs_sheet)
    unsubs = get_table(unsub_sheet)

    return subs, unsubs


def split_date_iso(date):
    d = [int(a) for a in re.split("\/|\s|:", date)] # DD, MM, YYYY, hh, mm, ss

    return d[2], d[1], d[0], d[3], d[4], d[5] # YYYY, MM, DD, hh, mm, ss


def get_timestamp(object, config):
    date_key = config["sheet"]["columns"]["date"]

    return datetime(*split_date_iso(object[date_key])).timestamp()


def filter_mailing_list(subs, unsubs, config):
    mail_key = config["sheet"]["columns"]["mail"]
    mailing_list = []

    for sub in subs[::-1]:
        jump = False
        for contact in mailing_list:
            if contact[mail_key] == sub[mail_key]:
                jump = True
                break

        if jump == True:
            continue

        is_subscribed = True
        for unsub in unsubs[::-1]:
            if unsub[mail_key] == sub[mail_key]:
                sub_timestamp = get_timestamp(sub, config)
                unsub_timestamp = get_timestamp(unsub, config)

                if (unsub_timestamp - sub_timestamp > 0):
                    is_subscribed = False
                    break

        if is_subscribed:
            mailing_list.append(sub)

    return mailing_list[::-1]


def build_message(user, config):
    user_config = dict(config)

    for key, value in user.items():
        user_config["props"][f"user_{key}"] = value

    mail_html, mail_text, meta = build_feed(user_config)

    message = MIMEMultipart("alternative")
    message["to"] = user[config["sheet"]["columns"]["mail"]]
    message["From"] = meta["name"]
    message["subject"] = meta["subject"]

    text_mime = MIMEText(mail_text, "text")
    html_mime = MIMEText(mail_html, "html")

    message.attach(text_mime)
    message.attach(html_mime)

    return {"raw": urlsafe_b64encode(message.as_bytes()).decode()}


def dispatch_messages(mailing_list, credentials, config, quiet=False):
    size = len(mailing_list)
    index = 1

    with build("gmail", "v1", credentials=credentials) as service:
        for user in mailing_list:
            message = build_message(user, config)
            username = user[config["sheet"]["columns"]["name"]]
            response = service.users().messages().send(userId="me", body=message).execute()

            if not quiet:
                print(f"Sending {index} of {size} to {username}...")

            index += 1


def has_argv(*argvs):
    return any([a in argv for a in argvs])


if __name__ == "__main__":
    config = get_config()
    credentials = atuth(SCOPES)

    is_test = has_argv("--test", "-t")

    if is_test:
        mailing_list = [config["test_user"]]
    else:
        subscribers, unsubscribers = fetch_subscribers_data(credentials, config)
        mailing_list = filter_mailing_list(subscribers, unsubscribers, config)

    build_test()

    do_send = input("Send? (yes/no) ")

    if do_send.lower() in ("y", "yes"):
        dispatch_messages(mailing_list, credentials, config, is_test)
        print("Newsletter launched successfully!")
