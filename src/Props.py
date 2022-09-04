import __main__
from ipywidgets import Widget

import pandas as pd


class Props:
    user_props = {}

    @staticmethod
    def user_prop(func: function):
        Props.user_props[func.__name__] = func

        return func

    @staticmethod
    def get_props(user: pd.Series):
        return Props.__get_static_props().update(Props.__get_user_props(user))

    @staticmethod
    def __get_static_props():
        return {
            name: Props.__get_value(value)
            for name, value in vars(__main__).items()
            if Props.__filter_name(name)
        }

    @staticmethod
    def __get_value(value: any):
        if isinstance(value, Widget):
            return value.value

        return value

    @staticmethod
    def __filter_name(name: str):
        if name == "users":
            return False

        if name.startswith("_"):
            return False

        return True

    @staticmethod
    def __get_user_props(user: pd.Series):
        return user.to_dict().update(Props.__get_user_dynamic_props(user))

    @staticmethod
    def __get_user_dynamic_props(user: pd.Series):
        return {key: handler(user) for key, handler in Props.user_props.items()}
