import json
from pathlib import Path

import __main__


class Workspace:
    HIDDEN_FILES = (
        "**/env",
        "**/src",
        "**/.vscode",
        "**/public/image",
        "**/public/template",
        ".gitignore",
        "requirements.txt",
    )

    @staticmethod
    def get_ipynb_file():
        return Path(vars(__main__)["__vsc_ipynb_file__"])

    @staticmethod
    def get_ipynb():
        with open(Workspace.get_ipynb_file(), "r", encoding="utf-8") as notebook_file:
            notebook = json.load(notebook_file)

        return notebook

    @staticmethod
    def get_html_source():
        ipynb = Workspace.get_ipynb()
        source = []

        for cell in ipynb["cells"]:
            cell_source = cell["source"]

            if len(cell_source) > 1 and cell_source[0] == "%%script html\n":
                source.extend(cell["source"][1:])

        return "".join(source)

    @staticmethod
    def show_source(state=True):
        with open(".vscode/settings.json", "r") as settings_file:
            settings = json.load(settings_file)

        for key in Workspace.HIDDEN_FILES:
            settings["files.exclude"][key] = not state

        with open(".vscode/settings.json", "w") as settings_file:
            json.dump(settings, settings_file, indent=4)
