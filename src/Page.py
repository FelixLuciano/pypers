import __main__
import cssutils
from bs4 import BeautifulSoup
from jinja2 import BaseLoader, Environment
from ipywidgets import Widget

from .Jupyter import Jupyter
from .Preview import Preview


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
            if name != 'users' and not name.startswith('_'):
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
            if not node.has_attr('style'):
                node['style'] = ''

            style = cssutils.css.CSSStyleDeclaration(node['style'])

            for rule_property in rule.style:
                style.removeProperty(rule_property.name)
                style.setProperty(rule_property.name, rule_property.value)

            node['style'] = style.cssText


    @staticmethod
    def get_template():
        html_source = Jupyter.get_html_source()
        source = BeautifulSoup(html_source, "html.parser")
        template = source.find('template')
        style = cssutils.parseString(source.find('style').text)

        Page.apply_styleSheet(style, template)

        for node in template.select('[class]'):
            del node['class']

        return ''.join(map(str, template.children))


    @staticmethod
    def render(user):
        template = Environment(loader=BaseLoader).from_string(Page.get_template())
        props = Page.get_props(user)

        return template.render(**props)


    @staticmethod
    def preview():
        Preview.display(Page)
