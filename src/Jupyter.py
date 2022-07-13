import json

import __main__


class Jupyter:
    @staticmethod
    def get_ipynb():
        filename = vars(__main__)['__vsc_ipynb_file__']

        with open(filename, 'r', encoding='utf-8') as file:
            notebook = json.load(file)

        return notebook


    @staticmethod
    def get_html_source():
        ipynb = Jupyter.get_ipynb()
        source = []

        for cell in ipynb['cells']:
            if cell['source'][0] == '%%script html\n':
                source.extend(cell['source'][1:])

        return ''.join(source)
