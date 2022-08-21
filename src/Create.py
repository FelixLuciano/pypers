import json
from pathlib import Path


class Create:
    BASEDIR = Path("pages")
    TEMPLATE_FILENAME = Path("public", "template", "New Page.ipynb")

    def __init__(self, filename: Path):
        self.filename = self.BASEDIR.joinpath(filename).with_suffix(
            filename.suffix + ".ipynb"
        )
        self.stem = filename.stem

        count = 0
        while self.filename.exists():
            count += 1
            self.filename = self.filename.with_stem(" ".join([self.stem, str(count)]))

    def create_file(self):
        self.filename.parent.mkdir(exist_ok=True, parents=True)

        with open(Create.TEMPLATE_FILENAME, "r", encoding="utf-8") as template_file:
            template = json.load(template_file)

        template["cells"][0]["source"] = f"# **{self.stem}**"

        with open(self.filename, "w", encoding="utf-8") as page_file:
            json.dump(template, page_file)
