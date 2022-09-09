from os.path import getmtime
from pathlib import Path

import cssutils
from bs4 import BeautifulSoup
from jinja2 import BaseLoader, Environment, TemplateNotFound

from .Style import Style


class Parser:
    @staticmethod
    def parse(source: str):
        template = Parser.__get_styled_template(source)

        return Parser.__get_environment().from_string(template)

    @staticmethod
    def __get_styled_template(source):
        tree = Parser.__get_styled_template_tree(source)

        return Parser.__join_children_html(tree)

    @staticmethod
    def __get_styled_template_tree(source):
        templates, stylesheets = Parser.__get_templates_stylesheets(source)

        if stylesheets != None:
            Style.apply_styleSheet(templates, stylesheets)
            Parser.__remove_tree_class_declarations(templates)

        return templates

    @staticmethod
    def __get_templates_stylesheets(source: str):
        node_tree = BeautifulSoup(source, "html.parser")
        template_nodes = node_tree.find("template")
        style_nodes = node_tree.find("style")
        stylesheets = None

        if template_nodes == None:
            raise Exception("No template cell")
        elif style_nodes != None:
            stylesheets = cssutils.parseString(style_nodes.text)

        return template_nodes, stylesheets

    @staticmethod
    def __remove_tree_class_declarations(tree):
        for node in tree.select("[class]"):
            del node["class"]

    @staticmethod
    def __join_children_html(tree):
        return "".join(map(str, tree.children))

    @staticmethod
    def __get_environment():
        return Environment(loader=Parser.Loader())

    class Loader(BaseLoader):
        @staticmethod
        def get_source(environment, template):
            filename = Path(Path.cwd(), template)

            if not filename.exists():
                raise TemplateNotFound(str(filename))

            mtime = getmtime(filename)

            with open(filename) as source_file:
                source = source_file.read()

            return source, filename, lambda: mtime == getmtime(filename)
