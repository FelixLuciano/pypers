import json

import __main__


class Notebook:
    def __init__(self, path):
        self.path = path

    @staticmethod
    def get_current():
        path = Notebook.__get_current_path()

        return Notebook(path)

    def get_ipynb(self):
        with open(self.path, "r", encoding="utf-8") as ipynb:
            return json.load(ipynb)

    def get_html_source(self):
        ipynb = self.get_ipynb()
        source = []

        for cell in ipynb["cells"]:
            cell_source = cell["source"]

            if len(cell_source) > 1 and cell_source[0] == "%%script html\n":
                source.extend(cell_source[1:])

        return "".join(source)

    @staticmethod
    def __get_current_path():
        scope = vars(__main__)

        if "__vsc_ipynb_file__" not in scope:
            raise Exception("Pypers only work at VS Code Jupyter!")

        return scope["__vsc_ipynb_file__"]
