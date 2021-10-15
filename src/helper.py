import datetime
import re
import markdown


MONTHS = (None, "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro")


def get_date():
    now = datetime.datetime.now()
    day, month, year = now.day, MONTHS[now.month], now.year

    return day, month, year


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


def apply_css(html, css):
    rules = get_css_rules(css)
    applied = apply_css_rules(html, rules)

    return applied


def build_mail (config, templates):
    title = f"{config['news']['name']} - {config['news']['subject']}"

    with open("src/page/news.md", "r", encoding="utf-8") as md_file:
        mail_md = md_file.read()

    with open("src/page/style.css", "r", encoding="utf-8") as css_file:
        mail_css = css_file.read()

    with open("src/page/template.html", "r", encoding="utf-8") as html_file:
        mail_template = html_file.read()

    mail_md = mail_md.format(**templates)
    mail_content = markdown.markdown(mail_md)
    styled_content = apply_css(mail_content, mail_css)
    mail_html = mail_template.format(title, styled_content)

    return mail_html


def extract_text(html):
    re_sub_tags = r"<.*?>"
    re_sub_nl = r"\n+"

    text = re.sub(re_sub_tags, "", html, 0)
    clear = re.sub(re_sub_nl, "\n\n", text, 0).strip("\n")

    return clear


def valid_input(validator=str, prompt="", accept=None, reject=[], persist=True, apply=None):
    """https://gist.github.com/FelixLuciano/ab8f51dc6f2cb726418ef139b8dbd20f
    """
    while True:
        try:
            response = validator(input(prompt))
            normalized = apply(response) if apply != None else response
        except ValueError:
            if persist != False:
                print("Invalid input!")
            else:
                return None
        except KeyboardInterrupt:
            print("\nInput canceled!")
            return None
        else:
            if (accept == None or normalized in accept) and normalized not in reject:
                return response
            elif persist != False:
                print("Invalid input!")
            else:
                return None
