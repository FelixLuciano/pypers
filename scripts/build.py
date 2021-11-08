import datetime
import json
import os
import tempfile
import webbrowser
from html.parser import HTMLParser
from pathlib import Path

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
        style_rules = []

        if tag in self._styles_rules:
            style_rules.append(self._styles_rules[tag])
        
        for i, (attr, value) in enumerate(attrs):
            if attr == "style":
                style_rules.append(value)
                del attrs[i]
                continue

            elif attr == "class":
                for classe in value.split(" "):
                    selector = "." + classe

                    if selector in self._styles_rules:
                        style_rules.append(self._styles_rules[selector])

                del attrs[i]
                continue

        if len(style_rules) > 0:
            attrs.append(("style", "".join(style_rules)))

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

    return html_content, meta


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

    styles_rules = get_style_rules()
    styled_html = apply_css_rules(mail_html, styles_rules)

    return styled_html, meta


def preview_output(output, open_preview=True):
    path = os.path.abspath("build/output.html")

    if not os.path.exists("build"):
        os.makedirs("build")

    with open(path, "w", encoding="utf-8") as file:
        file.write(output)

    if open_preview:
        print("Opening preview...")
        webbrowser.open(path)


def delete_output():
    Path("build/output.html").unlink()
    Path("build").rmdir()


def build_html(config, save=False, open_preview=True):
    mail_html, meta = get_mail_html(config)

    if save:
        preview_output(mail_html, open_preview)

    return mail_html, meta


def get_config():
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return config


def build_test(config, open_preview=True):
    for key, value in config["test_user"].items():
        config["props"][f"user_{key}"] = value

    return build_html(config, True, open_preview)


if __name__ == "__main__":
    build_test(get_config())
