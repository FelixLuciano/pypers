import argparse
import json
import os
import sys
from pathlib import Path


def main(args):
    output_file = Path(f'pages/{args.path}.ipynb')

    if output_file.is_file():
        return 'A page with this name already exists!'

    output_file.parent.mkdir(exist_ok=True, parents=True)

    with open('public/template/new page.ipynb', 'r', encoding='utf-8') as template_file:
        template = json.load(template_file)

    template['cells'][0]['source'] = f'# **{output_file.stem}**'

    with open(output_file, 'w', encoding='utf-8') as page_file:
        json.dump(template, page_file)

    os.system(str(output_file.absolute()))

    return 0


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path',
        default='New page',
        help=f'Specify the location with create a new page (default: New page)'
    )

    return parser.parse_args()


if __name__ == '__main__':
    sys.exit(main(parse_arguments()))
