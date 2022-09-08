from types import FunctionType
from typing import Callable, TypeAlias

import pandas as pd


user_prop_calable_type: TypeAlias = Callable[[pd.Series], any]

class User_prop:
    def __init__(self, name:str, cb:user_prop_calable_type):
        self.name = name
        self.cb = cb

    def __call__(self, user:pd.Series):
        return self.get_value(user)

    def get_value(self, user:pd.Series):
        return self.cb(user)

    @staticmethod
    def define_decorator(name:str|user_prop_calable_type=None):
        def func(cb:user_prop_calable_type):
            prop_name = cb.__name__ if name == None else name
            return User_prop(prop_name, cb)

        if isinstance(name, FunctionType):
            (cb, name) = (name, None)
            return func(cb)

        return func
