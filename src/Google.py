import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Google:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        'https://www.googleapis.com/auth/gmail.readonly',
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]
    credentials = None
    userinfo = None


    @staticmethod
    def authenticate(_is_retry=False):
        if os.path.exists('token.json'):
            Google.credentials = Credentials.from_authorized_user_file('token.json', Google.SCOPES)

        if not Google.credentials or not Google.credentials.valid:
            if Google.credentials and Google.credentials.expired and Google.credentials.refresh_token:    
                try:
                    Google.credentials.refresh(Request())
                except Exception:
                    os.unlink('token.json')

                    if not _is_retry:
                        Google.authenticate(True)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', Google.SCOPES)
                Google.credentials = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(Google.credentials.to_json())

        Google.userinfo = Google.fetch_userinfo()


    @staticmethod
    def fetch_userinfo():
        return build(serviceName='oauth2', version='v2', credentials=Google.credentials).userinfo().get().execute()


    class Gmail:
        @staticmethod
        def get_service():
            Google.authenticate()

            return build(serviceName="gmail", version="v1", credentials=Google.credentials)


        @staticmethod
        def get_aliases():
            response = Google.Gmail.get_service().users().settings().sendAs().list(userId='me').execute()

            return [f"{alias['displayName']} <{alias['sendAsEmail']}>" for alias in response['sendAs']]


        @staticmethod
        def send(body):
            return Google.Gmail.get_service().users().messages().send(userId="me", body=body).execute()
