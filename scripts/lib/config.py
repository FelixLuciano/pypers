import datetime
import json
import math
import os
import re
import sys


def has_argv(*argv):
    return any([a in sys.argv for a in argv])

IS_TEST = has_argv("--test", "-t")


def _select_page():
    pages = [name for name in os.listdir(
        "pages") if os.path.isdir(os.path.join("pages", name))]
    pages_len = len(pages)

    if pages_len == 1:
        return f"pages/{pages[0]}/"

    pad = math.ceil(math.log10(len(pages)))

    for i, page in enumerate(pages, 1):
        index = str(i).rjust(pad, " ")

        print(f"{index}: {page}")

    while True:
        try:
            index = int(input(f"select the page: (1-{pages_len}) ")) - 1

            if index >= 0 and index < len(pages):
                page = pages[index]
                break
        except KeyboardInterrupt:
            exit()

    return f"pages/{page}/"

BASEDIR = _select_page()


with open(BASEDIR + "config.json", "r", encoding="utf-8") as config_file:
    CONFIG = json.load(config_file)


MARKDOWN_EXTENSIONS = ["meta", "md_in_html", "attr_list", "admonition"]


SELFCLOSING_TAGS = ("area", "base", "br", "col", "embed", "hr",
                    "img", "input", "link", "meta", "param", "source", "track", "wbr")
MATCH_COMMA = re.compile("\s*,\s*")
MATCH_SPACE = re.compile("\s+")


_now = datetime.datetime.now()
_MONTHS = (None, "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December")

DATE = {
    "day": _now.day,
    "month": _MONTHS[_now.month],
    "year": _now.year
}


JOIN_META = False


GOOGPE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

CAPTHCA_CODE_RANGE = 5
