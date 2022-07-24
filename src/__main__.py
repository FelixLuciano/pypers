import argparse
import sys
from pathlib import Path


def main(args):
    if args.action == "setup":
        import subprocess
        import venv

        venv.create("env", with_pip=True)
        subprocess.run([Path("env", "Scripts", "pip"), "-r", "requirements.txt"])

    elif args.action == "create":
        from os import startfile

        from Create import Create

        new_page = Create(args.dest)

        new_page.create_file()
        startfile(new_page.filename)

    elif args.action == "source":
        from Workspace import Workspace

        if args.show and not args.hide:
            Workspace.show_source(True)
        elif not args.show and args.hide:
            Workspace.show_source(False)

    return 0


def parse_arguments():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="action")
    source = subparser.add_parser("setup")
    source = subparser.add_parser("source")
    create = subparser.add_parser("create")

    source.add_argument(
        "--show",
        action="store_true",
        help=f"Show project source",
    )

    source.add_argument(
        "--hide",
        action="store_true",
        help=f"Hide project source",
    )

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
