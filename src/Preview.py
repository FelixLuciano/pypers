from pathlib import Path

import ipywidgets as widgets
from bs4 import BeautifulSoup
from IPython.display import HTML, display

import __main__

from .Page import Page
from .Preview_controls import Preview_controls


class Preview:
    PREVIEW_TEMPLATE_PATH = Path(__file__).parent.joinpath("data", "preview.html")

    @staticmethod
    def __get_preview_template():
        with open(
            Preview.PREVIEW_TEMPLATE_PATH, "r", encoding="utf-8"
        ) as template_file:
            return BeautifulSoup(template_file, "html.parser")

    @staticmethod
    def __wrap_preview_template(content):
        template = Preview.__get_preview_template()
        content_node = BeautifulSoup(content, "html.parser")
        anchor = template.select_one("page-preview")

        anchor.insert_after(content_node)
        anchor.decompose()

        return str(template)

    @staticmethod
    def display():
        out = widgets.Output()

        @Preview_controls.on_update
        def update():
            Preview_controls.disable()

            user = Preview_controls.get_selected_user()
            render = Page().render(user)
            preview = Preview.__wrap_preview_template(render)

            with out:
                out.clear_output(wait=True)
                display(HTML(preview))

            Preview_controls.enable()

        Preview_controls.init()
        Preview_controls.display()
        display(out)
        update()
