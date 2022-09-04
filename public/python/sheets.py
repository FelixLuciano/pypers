from functools import cache

import pandas as pd
from googleapiclient.discovery import build
from pypers import Google


Google.SCOPES.append("https://www.googleapis.com/auth/spreadsheets.readonly")


class Sheets:
    @cache
    @staticmethod
    def get_service():
        Google.authenticate()

        return build(serviceName="sheets", version="v4", credentials=Google.credentials)

    @staticmethod
    def fetch_table(spreadsheetId, range_, *args, **kwargs):
        sheets = Sheets.get_service().spreadsheets().values()
        response = sheets.get(spreadsheetId=spreadsheetId, range=range_).execute()
        values = response["values"]

        return pd.DataFrame(values[1:], columns=values[0], *args, **kwargs)
