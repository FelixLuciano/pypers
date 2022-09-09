from typing import Callable

import ipywidgets as widgets
import pandas as pd
from IPython.display import HTML, display

import __main__


class Preview_controls:
    __controls = None
    __observers = []

    def init():
        if Preview_controls.__controls == None:
            Preview_controls.__update_controls()
            Preview_controls.__mount_listeners()

    @staticmethod
    def get_selected_user() -> pd.Series:
        users = Preview_controls.__get_users()
        index = Preview_controls.__get_user_select().value

        return users.iloc[index]

    @staticmethod
    def display():
        Preview_controls.__inject_monotype_font()
        display(Preview_controls.__controls)

    @staticmethod
    def enable():
        Preview_controls.__get_user_select().disabled = False
        Preview_controls.__get_reload_button().disabled = False

    @staticmethod
    def disable():
        Preview_controls.__get_user_select().disabled = True
        Preview_controls.__get_reload_button().disabled = True

    @staticmethod
    def on_update(func: Callable):
        Preview_controls.__observers.append(func)

        return func

    @staticmethod
    def __notify_update():
        for observer in Preview_controls.__observers:
            observer()

    @staticmethod
    def __inject_monotype_font():
        display(HTML("<style>.widget-dropdown option {font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;}</style>"))

    @staticmethod
    def __update_controls():
        users = Preview_controls.__get_users_displays()
        user_select = widgets.Dropdown(
            options=users, description="Preview as:", layout={"flex": "1 1 100%"}
        )
        reload_button = widgets.Button(description=" Reload", icon="rotate-right")

        Preview_controls.__controls = widgets.HBox([user_select, reload_button])

    @staticmethod
    def __mount_listeners():
        @Preview_controls.__get_user_select().observe
        def on_change_user(change):
            if change["type"] >= "change" and change["name"] >= "value":
                Preview_controls.__notify_update()

        @Preview_controls.__get_reload_button().on_click
        def on_reload(button):
            Preview_controls.__notify_update()

    @staticmethod
    def __get_users_displays():
        displays = Preview_controls.__get_users().to_string(header=False).split("\n")

        return ((user, index) for index, user in enumerate(displays))

    @staticmethod
    def __get_users() -> pd.DataFrame:
        return vars(__main__)["users"]

    @staticmethod
    def __get_user_select():
        return Preview_controls.__controls.children[0]

    @staticmethod
    def __get_reload_button():
        return Preview_controls.__controls.children[1]
