import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .config import *


CREDENTIALS = None

if os.path.exists("token.json"):
    CREDENTIALS = Credentials.from_authorized_user_file("token.json", GOOGPE_API_SCOPES)

if not CREDENTIALS or not CREDENTIALS.valid:
    if CREDENTIALS and CREDENTIALS.expired and CREDENTIALS.refresh_token:
        CREDENTIALS.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", GOOGPE_API_SCOPES)
        CREDENTIALS = flow.run_local_server(port=0)

    with open("token.json", "w") as token:
        token.write(CREDENTIALS.to_json())


SHEETS_SERVICE = build(serviceName="sheets", version="v4", credentials=CREDENTIALS)


GMAIL_SERVICE = build(serviceName="gmail", version="v1", credentials=CREDENTIALS)


_AUTH_SERVICE = build(serviceName='oauth2', version='v2', credentials=CREDENTIALS)
USER_INFO = _AUTH_SERVICE.userinfo().get().execute()
