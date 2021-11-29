import os
import webbrowser
from pathlib import Path

from lib.config import *
from lib.page import Page


def save_output(output, open_preview=True):
    path = os.path.abspath("build/output.html")

    if not os.path.exists("build"):
        os.makedirs("build")

    with open(path, "w", encoding="utf-8") as file:
        file.write(output)

    if open_preview:
        print("Opening preview...")
        webbrowser.open(path)


def delete_output():
    Path("build/output.html").unlink()
    Path("build").rmdir()


def build(open_preview=True, props={}):
    page = Page()

    try:
        output = page.get_page(props)
        save_output(output, open_preview)

        return output
    except BaseException as error:
        print(error)
    else:
        save_output(page.page, open_preview)

        return output


if __name__ == "__main__":
    build()
