from os.path import getmtime
from pathlib import Path

import __main__
import cssutils
from bs4 import BeautifulSoup
from ipywidgets import Widget
from jinja2 import BaseLoader, Environment, TemplateNotFound
from jinja_markdown import MarkdownExtension

from .Workspace import Workspace
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
    def apply_styleSheet(stylesheet, tree):
        for rule in stylesheet:
            if isinstance(rule, cssutils.css.CSSImportRule):
                Page.apply_styleSheet(rule.styleSheet, tree)

            elif isinstance(rule, cssutils.css.CSSStyleRule):
                Page.apply_stylesheet_rule(rule, tree)

    @staticmethod
    def apply_stylesheet_rule(rule, tree):
        for node in tree.select(rule.selectorText):
            if not node.has_attr("style"):
                node["style"] = ""

            style = cssutils.css.CSSStyleDeclaration(node["style"])

            for rule_property in rule.style:
                style.removeProperty(rule_property.name)
                style.setProperty(rule_property.name, rule_property.value)

            node["style"] = style.cssText

    @staticmethod
    def get_template():
        env = Environment(loader=Page.Loader())
        html_source = Workspace.get_html_source()
        source = BeautifulSoup(html_source, "html.parser")
        template = source.find("template")
        style = cssutils.parseString(source.find("style").text)

        env.add_extension(MarkdownExtension)
        Page.apply_styleSheet(style, template)

        for node in template.select("[class]"):
            del node["class"]

        template_str = "".join(map(str, template.children))

        return env.from_string(template_str)

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
