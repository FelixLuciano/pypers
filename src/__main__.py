import argparse
import sys
from pathlib import Path


def main(args):
    if args.action == "create":
        from Page_file import Page_file

        new_page = Page_file(args.dest)

        new_page.make_from_template()
        new_page.startfile()
        print(f"Created {new_page.path.absolute()}")

    return 0


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    create = subparser.add_parser("create")

    create.add_argument(
        "dest",
        type=Path,
        default="New Page",
        help=f"Specify the location with create a new page (default: New page)",
    )

    return parser.parse_args()


if __name__ == "__main__":
    exit_code = 0

    try:
        exit_code = main(parse_arguments())
    except KeyboardInterrupt:
        pass
    except Exception as error:
        exit_code = error
    finally:
        sys.exit(exit_code)
