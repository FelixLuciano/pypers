from html.parser import HTMLParser
from json import load
from os.path import exists

from .config import *


class StyleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

        self.styles = {}
        self.html = []


    def feed(self, data):
        self.rawdata = self.rawdata + data
        self.html = []
        self.goahead(0)


    def add(self, filename):
        if exists(filename):
            with open(filename, "r", encoding="utf-8") as styles_file:
                for selector, props in load(styles_file).items():
                    if selector in self.styles:
                        self.styles[selector].update(props)
                    else:
                        self.styles[selector] = props


    @staticmethod
    def match_selector(selector, tag, classes=[]):
        rules = MATCH_COMMA.split(selector)

        for rule in rules:
            is_tag_rule = not rule.startswith(".")
            rule_classes = rule.split(".")

            if is_tag_rule and rule_classes[0] == tag or not is_tag_rule:
                if all(rule_class in classes for rule_class in rule_classes[1:]):
                    return True

        return False


    def get_style_attr(self, tag, class_attr=""):
        classes = MATCH_SPACE.split(class_attr)

        props = {}

        for selector, style in self.styles.items():
            if self.match_selector(selector, tag, classes):
                props.update(style)

        return "".join([p+":"+v+";" for p, v in props.items()])


    def handle_starttag(self, tag, attrs):
        style_attr = []

        tag_styles = self.get_style_attr(tag)
        if tag_styles:
            style_attr.append(tag_styles)

        for i, (attr, value) in enumerate(attrs):
            if attr == "style":
                style_attr.append(value)
                del attrs[i]
                continue

            elif attr == "class":
                class_styles = self.get_style_attr(tag, value)
                if class_styles:
                    style_attr.append(class_styles)
                del attrs[i]
                continue

        if len(style_attr) > 0:
            attrs.append(("style", "".join(style_attr)))

        self.html.append("<" + tag)

        for attr, value in attrs:
            self.html.append(f" {attr}=\"{value}\"")

        if tag in SELFCLOSING_TAGS:
            self.html.append(" /")

        self.html.append(">")


    def handle_endtag(self, tag):
        if tag not in SELFCLOSING_TAGS:
            self.html.append(f"</{tag}>")


    def handle_data(self, data):
        self.html.append(data)


    def to_string(self):
        return "".join(self.html)
