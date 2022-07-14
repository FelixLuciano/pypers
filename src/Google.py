import os

import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Google:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]
    credentials = None
    userinfo = None


    @staticmethod
    def authenticate():
        if os.path.exists('token.json'):
            Google.credentials = Credentials.from_authorized_user_file('token.json', Google.SCOPES)
        if not Google.credentials or not Google.credentials.valid:
            if Google.credentials and Google.credentials.expired and Google.credentials.refresh_token:
                Google.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', Google.SCOPES)
                Google.credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(Google.credentials.to_json())

        
        Google.userinfo = Google.fetch_userinfo()


    @staticmethod
    def fetch_userinfo():
        return build(serviceName='oauth2', version='v2', credentials=Google.credentials).userinfo().get().execute()


    @property
    def gmail():
        Google.authenticate()

        return build(serviceName="gmail", version="v1", credentials=Google.credentials)
