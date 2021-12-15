import os
import argparse


parser = argparse.ArgumentParser(description='Pynews')

parser.add_argument("--dir")
parser.add_argument("--name")

ARGS = parser.parse_args()


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

# Hello World!

Welcome to {{name}} page.

Computed property: {{computed}}.
"""

styles = """\
{
    "h1": {
        "color": "#2b7ea0"
    }
}\
"""

styles = """\
{
    "h1": {
        "color": "#2b7ea0"
    }
}\
"""

computed = """\
def update(props):
    \"\"\"
    Updates props on each build (i.e. for every user).
    \"\"\"
    # Do something...

    return props

# Example of computed props: First 10 members of fibonacci series.
# Private variables starting with "_" are not set as props.
_fibonacci = [1, 1]
_size = 10

for i in range(len(_fibonacci), _size):
    _fibonacci.append(sum(_fibonacci[-2:]))

computed = ", ".join([str(a) for a in _fibonacci])
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

    with open(basedir + "props.py", "w", encoding="utf-8") as props_file:
        props_file.write(computed)


if __name__ == "__main__":
    if not ARGS.name:
        name = input("Page name: ")
    else:
        name = ARGS.name

    create_page(name)
