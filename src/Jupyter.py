import json
from pathlib import Path

import __main__


class Jupyter:
    @staticmethod
    def get_ipynb_file():
        return Path(vars(__main__)['__vsc_ipynb_file__'])


    @staticmethod
    def get_ipynb():
        with open(Jupyter.get_ipynb_file(), 'r', encoding='utf-8') as file:
            notebook = json.load(file)

        return notebook


    @staticmethod
    def get_html_source():
        ipynb = Jupyter.get_ipynb()
        source = []

        for cell in ipynb['cells']:
            cell_source = cell['source']

            if len(cell_source) > 1 and cell_source[0] == '%%script html\n':
                source.extend(cell['source'][1:])

        return ''.join(source)
