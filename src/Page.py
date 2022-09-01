from os.path import getmtime
from pathlib import Path

import __main__
import cssutils
from bs4 import BeautifulSoup
from ipywidgets import Widget
from jinja2 import BaseLoader, Environment, TemplateNotFound

from .Workspace import Workspace
from .Parser import Parser
from .Preview import Preview
from .Send import Send


class Page:
    user_props = {}

    @staticmethod
    def user_prop(func):
        Page.user_props[func.__name__] = func

        return func

    @staticmethod
    def get_props(user):
        props = {}

        for name, value in vars(__main__).items():
            if name != "users" and not name.startswith("_"):
                if isinstance(value, Widget):
                    props[name] = value.value
                else:
                    props[name] = value

        props.update(user)
        props.update({key: handler(user) for key, handler in Page.user_props.items()})

        return props

    @staticmethod
    def get_template():
        return Parser.parse(Workspace.get_html_source())

    @staticmethod
    def render(user):
        return Page.get_template().render(**Page.get_props(user))

    @staticmethod
    def preview():
        Preview.display(Page)

    @staticmethod
    def send():
        return Send.display(Page)

    class Loader(BaseLoader):
        def get_source(self, environment, template):
            filename = Path(Path.cwd(), template)

            if not filename.exists():
                raise TemplateNotFound(str(filename))

            mtime = getmtime(filename)

            with open(filename) as source_file:
                source = source_file.read()

            return source, filename, lambda: mtime == getmtime(filename)
