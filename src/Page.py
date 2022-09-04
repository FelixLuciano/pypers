import __main__

from .Notebook import Workspace
from .Parser import Parser
from .Props import Props


class Page():
    def __init__(self):
        self.update_template()

    def update_template(self):
        source = Workspace.get_html_source()
        self.template = Parser.parse(source)

    def render(self, user):
        return self.template.render(**Props.get_props(user))
