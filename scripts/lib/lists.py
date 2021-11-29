import csv
import datetime
import re

from .config import *
from .services import SHEETS_SERVICE


def to_table(values):
    header = [h.replace(" ", "_") for h in values[0]]
    body = values[1:]

    return list(dict(zip(header, row)) for row in body)


def split_date_iso(date):
    d = [int(a) for a in re.split("\/|\s|:", date)]  # DD, MM, YYYY, hh, mm, ss

    return d[2], d[1], d[0], d[3], d[4], d[5]       # YYYY, MM, DD, hh, mm, ss


def get_timestamp(object):
    return datetime.datetime(*split_date_iso(object["Date"])).timestamp()


def filter_mailing_list(joins, leaves):
    mailing_list = []

    for join in joins[::-1]:
        jump = False
        for contact in mailing_list:
            if contact["Email"] == join["Email"]:
                jump = True
                break

        if jump == True:
            continue

        is_joined = True
        for leave in leaves[::-1]:
            if leave["Email"] == join["Email"]:
                join_timestamp = get_timestamp(join)
                leave_timestamp = get_timestamp(leave)

                if (leave_timestamp - join_timestamp > 0):
                    is_joined = False
                    break

        if is_joined:
            mailing_list.append(join)

    return mailing_list[::-1]


def load_from_file():
    with open(BASEDIR + "joins.csv") as joins_file:
        joins_list = csv.reader(joins_file, delimiter=";", quotechar='"')
        joins = to_table(list(joins_list))

    if os.path.exists(BASEDIR + "leaves.csv"):
        with open(BASEDIR + "leaves.csv") as leaves_file:
            leaves_list = csv.reader(leaves_file, delimiter=";", quotechar='"')
            leaves = to_table(list(leaves_list))

        print(joins, leaves)
        return filter_mailing_list(joins, leaves)

    return joins


def load_from_sheets():
    sheet_id = CONFIG["mailing_list"]["id"]

    with SHEETS_SERVICE as service:
        sheets = service.spreadsheets().values()

        joins_sheet = sheets.get(
            spreadsheetId=sheet_id, range="joins").execute()
        joins = to_table(joins_sheet["values"])

        if CONFIG["mailing_list"]["leaves_sheet"]:
            leaves_sheet = sheets.get(
                spreadsheetId=sheet_id, range="leaves").execute()
            leaves = to_table(leaves_sheet["values"])

            return filter_mailing_list(joins, leaves)

    return joins


if IS_TEST:
    MAILING_LIST = [CONFIG["props"]]
else:
    if "mailing_list" not in CONFIG or CONFIG["mailing_list"]["type"] == "csv":
        MAILING_LIST = load_from_file()
    elif CONFIG["mailing_list"]["type"] == "sheets":
        MAILING_LIST = load_from_sheets()
