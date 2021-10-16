import os
import re
import json
import datetime
import markdown
import webbrowser


def get_css():
    with open("src/page/style.css", "r", encoding="utf-8") as css_file:
        css_rules = css_file.read()

    return css_rules


def get_css_rules(css):
    re_match = r"(?:\w+)|(?:(?<={)[^{}]+(?=}))"
    re_sub = r"[\s\n]+"
    matches = re.findall(re_match, css, re.MULTILINE | re.DOTALL)
    matches_formated = [re.sub(re_sub, " ", match, 0).strip() for match in matches]
    selector_rules = zip(matches_formated[::2], matches_formated[1::2])

    return selector_rules


def apply_css_rules(html, rules):
    new_html = str(html)

    for selector, rule in rules:
        stf_sub = f"(?<=<{selector}).*(?=>.*?</{selector}>)|(?<=<{selector}).*(?=>)"
        re_sub = re.compile(stf_sub, re.MULTILINE)
        subst = f" style=\"{rule}\"\\g<0>"
        new_html = re.sub(re_sub, subst, new_html, 0)
    return new_html


def get_meta(meta_dict):
    meta_flat = {}

    for key in meta_dict:
        meta_flat[key] = ", ".join(meta_dict[key])

    return meta_flat


def get_mail_content():
    with open("src/page/news.md", "r", encoding="utf-8") as md_file:
        md_content = md_file.read()

    md = markdown.Markdown(extensions=["meta"])
    html_content = md.convert(md_content)
    meta = get_meta(md.Meta)

    css = get_css()
    css_rules = get_css_rules(css)
    styled_content = apply_css_rules(html_content, css_rules)

    return styled_content, meta


def get_template():
    with open("src/page/template.html", "r", encoding="utf-8") as html_file:
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
        **config["template"],
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


def extract_html_text(html):
    re_sub_tags = r"<.*?>"
    re_sub_nl = r"\n+"

    text = re.sub(re_sub_tags, "", html, 0)
    clear = re.sub(re_sub_nl, "\n\n", text, 0).strip("\n")

    return clear


def save_output(filename, data):
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(data)


def build_html(config, save = False):
    mail_html, meta = get_mail_html(config)

    if save:
        save_output("build/output.html", mail_html)

    return mail_html, meta


def build_text(html, save = False):
    mail_text = extract_html_text(html)

    if save:
        save_output("build/output.txt", mail_text)

    return mail_text


def build(config, open_preview = False):
    mail_html, meta = build_html(config, open_preview)
    mail_text = build_text(mail_html)

    if open_preview:
        print("Abrindo visualização prévia...")
        webbrowser.open(os.path.abspath("build/output.html"))

    return mail_html, mail_text, meta


def get_config():
    with open("config.json", "r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return config


if __name__ == "__main__":
    config = get_config()
    build(config, True)
