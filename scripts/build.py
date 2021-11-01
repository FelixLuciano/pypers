import datetime
import json
import os
import tempfile
import webbrowser
from html.parser import HTMLParser

import markdown

MARKDOWN_EXTENSIONS = ["meta", "attr_list"]


def get_style_rules():
    with open("src/styles.json", "r", encoding="utf-8") as styles_file:
        styles_rules = json.load(styles_file)

    for selector, rules in styles_rules.items():
        rules_str = ""

        for prop, value in rules.items():
            rules_str += f"{prop}:{value};"

        styles_rules[selector] = rules_str

    return styles_rules


class StyleRulesParser(HTMLParser):
    def __init__(self, styles_rules):
        super().__init__()
        
        self._selfclosing_tags = ("area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr")
        self._styles_rules = styles_rules
        self._html = ""

    def handle_starttag(self, tag, attrs):
        if tag in self._styles_rules:
            rules = self._styles_rules[tag]
            
            for i, (attr, value) in enumerate(attrs):
                if attr == "style":
                    rules += value
                    del attrs[i]
                    break

            attrs.append(("style", rules))

        self._html += f"<{tag}"

        for attr, value in attrs:
            self._html += f" {attr}=\"{value}\""

        if tag in self._selfclosing_tags:
            self._html += " /"

        self._html += ">"

    def handle_endtag(self, tag):
        if tag not in self._selfclosing_tags:
            self._html += f"</{tag}>"

    def handle_data(self, data):
        self._html += data

    def to_string(self):
        return self._html


def apply_css_rules(html, rules):
    parser = StyleRulesParser(rules)
    parser.feed(html)

    return parser.to_string()


def get_meta(meta_dict):
    meta_flat = {}

    for key in meta_dict:
        meta_flat[key] = ", ".join(meta_dict[key])

    return meta_flat


def get_mail_content():
    with open("src/news.md", "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
    html_content = md.convert(md_content)
    meta = get_meta(md.Meta)

    styles_rules = get_style_rules()
    styled_content = apply_css_rules(html_content, styles_rules)

    return styled_content, meta


def get_template():
    with open("src/template.html", "r", encoding="utf-8") as html_file:
        html_template = html_file.read()

    return html_template


def get_date():
    MONTHS = (None, "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")

    now = datetime.datetime.now()
    day, month, year = now.day, MONTHS[now.month], now.year

    return day, month, year


def get_template_data(config, meta):
    day, month, year = get_date()

    template_data = {
        "day": day,
        "month": month,
        "year": year,
        **config["props"],
        **meta
    }

    return template_data


def get_mail_html (config):
    mail_content, meta = get_mail_content()
    mail_template = get_template()
    template_data = get_template_data(config, meta)
    
    mail_base = mail_template.format(content = mail_content)
    mail_html = mail_base.format(**template_data)

    return mail_html, meta


class InnerText_Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        
        self._blockLevel_tags = ("address", "article", "aside", "blockquote", "canvas", "dd", "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "noscript", "ol", "p", "pre", "section", "table", "tfoot", "ul", "video")
        self._text = ""

    def handle_endtag(self, tag):
        if tag in self._blockLevel_tags:
            self._text += "\n"

    def handle_data(self, data):
        self._text += data

    def to_string(self):
        return self._text


def extract_html_text(html):
    parser = InnerText_Parser()
    parser.feed(html)

    return parser.to_string()


def preview_output(output):
    fd, path = tempfile.mkstemp(suffix=".html")
    
    with os.fdopen(fd, "w", encoding="utf-8") as temp:
        temp.write(output)

    print("Opening preview...")
    webbrowser.open(path)


def build_html(config, preview=False):
    mail_html, meta = get_mail_html(config)

    if preview:
        preview_output(mail_html)

    return mail_html, meta


def build_feed(config, preview=False):
    mail_html, meta = build_html(config, preview)
    mail_text = extract_html_text(mail_html)

    return mail_html, mail_text, meta


def get_config():
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return config


def build_test(config):
    for key, value in config["test_user"].items():
        config["props"][f"user_{key}"] = value

    build_feed(config, True)


if __name__ == "__main__":
    config = get_config()
    
    build_test(config)
