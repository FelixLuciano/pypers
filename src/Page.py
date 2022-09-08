import __main__

from .Notebook import Notebook
from .Parser import Parser
from .Props import Props


class Page:
    def __init__(self):
        self.__notebook = Notebook.get_current()

        self.update_template()

    def update_template(self):
        source = self.__notebook.get_html_source()
        self.template = Parser.parse(source)

    def render(self, user):
        return self.template.render(**Props.get_props(user))
