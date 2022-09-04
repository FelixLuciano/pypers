from pathlib import Path

import ipywidgets as widgets
from bs4 import BeautifulSoup
from IPython.display import HTML, clear_output, display

import __main__
from .Preview_controls import Preview_coltrols
from .Page import Page


class Preview:
    PREVIEW_TEMPLATE_PATH = Path(__file__).parent.joinpath("data", "Preview_coltrols.html")

    @staticmethod
    def __get_preview_template():
        with open(
            Preview_coltrols.PREVIEW_TEMPLATE_PATH, "r", encoding="utf-8"
        ) as template_file:
            return BeautifulSoup(template_file, "html.parser")

    @staticmethod
    def __wrap_preview_template(content):
        template = Preview_coltrols.__get_preview_template()
        anchor = template.select_one("page-preview")

        anchor.insert_after(content)
        anchor.decompose()

        return str(template)

    @staticmethod
    def display():
        Preview_coltrols.__update_controls()

        user_select = Preview_coltrols.__get_user_select()
        reload_button = Preview_coltrols.__get_reload_button()

        def update():
            Preview_coltrols.disable()

            user = Preview_coltrols.get_selected_user()
            render = Page().render(user)
            preview = Preview.__wrap_preview_template(render)

            clear_output()
            Preview_coltrols.display()
            display(HTML(preview))
            Preview_coltrols.enable()

        @user_select.observe
        def on_change_user(change):
            if change["type"] >= "change" and change["name"] >= "value":
                update()

        @reload_button.on_click
        def on_reload(button):
            update()

        update()
