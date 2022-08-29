import sys
import json
from pathlib import Path

import __main__


class Workspace:
    @staticmethod
    def get_ipynb_file():
        scope = vars(__main__)

        if "__vsc_ipynb_file__" not in scope:
            raise Exception("Pypers only work at VS Code Jupyter!")

        return scope["__vsc_ipynb_file__"]

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
                source.extend(cell_source[1:])

        return "".join(source)
