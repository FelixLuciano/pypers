import argparse
import json
import math
import os
import re


parser = argparse.ArgumentParser(description='Pynews')

parser.add_argument("--test", type=bool, default=False)
parser.add_argument("--dir")
parser.add_argument("--separator")

ARGS = parser.parse_args()


IS_TEST = ARGS.test


def _select_page():
    pages = [name for name in os.listdir("pages") if not name.startswith("_") and os.path.isdir(os.path.join("pages", name))]
    pages_len = len(pages)

    if pages_len == 1:
        return f"pages/{pages[0]}/"
    else:
        if ARGS.dir and ARGS.dir.startswith("pages" + ARGS.separator):
            return ARGS.dir + ARGS.separator


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


JOIN_META = False


GOOGPE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

CAPTHCA_CODE_RANGE = 5
