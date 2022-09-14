from functools import cache
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class Google:
    __credentials = None
    __scopes = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ]
    @staticmethod
    def get_credentials():
        return Google.__credentials

    @cache
    @staticmethod
    def authenticate(_is_retry=False):
        credentials_file = Path("credentials.json")
        token_file = Path("token.json")

        if token_file.exists():
            Google.__credentials = Credentials.from_authorized_user_file(
                str(token_file), Google.__scopes
            )

        if not Google.__credentials or not Google.__credentials.valid:
            if (
                Google.__credentials
                and Google.__credentials.expired
                and Google.__credentials.refresh_token
            ):
                try:
                    Google.__credentials.refresh(Request())
                except Exception:
                    if token_file.exists():
                        token_file.unlink()
                    if not _is_retry:
                        Google.authenticate(True)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credentials_file), Google.__scopes
                )
                Google.__credentials = flow.run_local_server(port=0)
            with open(token_file, "w") as token:
                token.write(Google.__credentials.to_json())

    @staticmethod
    def extend_scopes(scopes):
        Google.__scopes.extend(scopes)

    @cache
    @staticmethod
    def get_userinfo():
        return (
            build(serviceName="oauth2", version="v2", credentials=Google.__credentials)
            .userinfo()
            .get()
            .execute()
        )

    class Gmail:
        @cache
        @staticmethod
        def get_service():
            Google.authenticate()

            return build(
                serviceName="gmail", version="v1", credentials=Google.get_credentials()
            )

        @cache
        @staticmethod
        def get_aliases():
            response = (
                Google.Gmail.get_service()
                .users()
                .settings()
                .sendAs()
                .list(userId="me")
                .execute()
            )

            return [
                f"{alias['displayName']} <{alias['sendAsEmail']}>"
                for alias in response["sendAs"]
            ]

        @staticmethod
        def send(body):
            return (
                Google.Gmail.get_service()
                .users()
                .messages()
                .send(userId="me", body=body)
                .execute()
            )
