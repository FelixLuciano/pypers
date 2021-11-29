import os

config = """\
{
    "mailing_list": {
        "type": "sheets/csv",
        "id": "FILE ID IF TYPE SHEETS",
        "leaves_sheet" : false
    },
    "props": {
        "Email": "TESTING E-MAIL ADDRESS"
    }
}\
"""

page = """\
name: {name}
subject: New page created

# Hello World

Welcome to {name} page!
"""

styles = """\
{
    "h1": {
        "color": "#2b7ea0"
    }
}\
"""


def create_page(name):
    basedir = f"pages/{name}/"

    os.mkdir(basedir)

    with open(basedir + "config.json", "w", encoding="utf-8") as config_file:
        config_file.write(config)

    with open(basedir + "page.md", "w", encoding="utf-8") as page_file:
        page_file.write(page.format(name=name))

    with open(basedir + "styles.json", "w", encoding="utf-8") as styles_file:
        styles_file.write(styles)


if __name__ == "__main__":
    name = input("Page name: ")

    create_page(name)
