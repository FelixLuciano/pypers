import pandas as pd
from ipywidgets import Widget

import __main__

from .User_prop import User_prop


class Props:
    @staticmethod
    def get_props(user:pd.Series):
        return {
            **Props.__get_scope_static_props(),
            **Props.__get_user_static_props(user),
            **Props.__get_user_dynamic_props(user),
        }

    @staticmethod
    def __get_scope_static_props():
        return {
            name: Props.__get_value(value)
            for name, value in Props.__get_defined_props().items()
            if Props.__filter_name(name)
        }

    @staticmethod
    def __get_defined_props():
        return vars(__main__)

    @staticmethod
    def __get_value(value):
        if isinstance(value, Widget):
            return value.value
        if isinstance(value, User_prop):
            return None

        return value

    @staticmethod
    def __filter_name(name: str):
        if name in ("In", "Out", "users"):
            return False

        if name.startswith("_"):
            return False

        return True

    @staticmethod
    def __get_user_static_props(user: pd.Series):
        return user.to_dict()

    @staticmethod
    def __get_user_dynamic_props(user: pd.Series):
        return {
            prop.name: prop.get_value(user)
            for prop in Props.__get_defined_props().values()
            if isinstance(prop, User_prop)
        }
