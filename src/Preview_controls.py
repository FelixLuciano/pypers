from pathlib import Path

import ipywidgets as widgets
from bs4 import BeautifulSoup
from bs4.element import Tag
from IPython.display import HTML, clear_output, display

import __main__
from .Page import Page


class Preview_controls:
    PREVIEW_TEMPLATE_PATH = Path(__file__).parent.joinpath("data", "preview.html")
    controls = None

    @staticmethod
    def get_selected_user():
        users = Preview_controls.__get_users()
        index = Preview_controls.__get_user_select().value

        return users[index]

    @staticmethod
    def __get_users():
        return vars(__main__)["users"]

    @staticmethod
    def __get_user_select():
        if Preview_controls.controls == None:
            Preview_controls.__update_controls()
        
        return Preview_controls.controls.children[0]

    @staticmethod
    def __get_reload_button():
        if Preview_controls.controls == None:
            Preview_controls.__update_controls()
        
        return Preview_controls.controls.children[1]

    @staticmethod
    def __update_controls():
        users = Preview_controls.__get_users_displays()
        user_select = widgets.Dropdown(
            options=users, description="Preview as:", layout={"flex": "1 1 100%"}
        )
        reload_button = widgets.Button(description=" Reload", icon="rotate-right")

        return widgets.HBox([user_select, reload_button])

    @staticmethod
    def __get_users_displays():
        displays = Preview_controls.__get_users().to_string(header=False).split("\n")

        return ((user, index) for index, user in enumerate(displays))

    @staticmethod
    def display():
        display(Preview_controls.controls)

    @staticmethod
    def enable():
        Preview_controls.__get_user_select().disabled = False
        Preview_controls.__get_reload_button().disabled = False

    @staticmethod
    def disable():
        Preview_controls.__get_user_select().disabled = True
        Preview_controls.__get_reload_button().disabled = True
