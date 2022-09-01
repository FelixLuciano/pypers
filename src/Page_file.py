import json
from os import startfile
from pathlib import Path


class Page_file:
    __TEMPLATE_FILENAME = Path(__file__).parent.joinpath("data", "New Page.ipynb")

    def __init__(self, path: Path):
        self.__name = path.name
        self.path = path

    def startfile(self):
        startfile(self.path)

    def make_from_template(self):
        ipynb = Page_file.__get_template_ipynb()

        self.__format_template_heading_name(ipynb)
        self.__make_file(ipynb)

    @staticmethod
    def __get_template_ipynb():
        with open(
            Page_file.__TEMPLATE_FILENAME, "r", encoding="utf-8"
        ) as template_file:
            return json.load(template_file)

    def __format_template_heading_name(self, ipynb: dict):
        ipynb["cells"][0]["source"] = f"# **{self.__name}**"

    def __make_file(self, ipynb: dict):
        self.__refresh_path_name()
        self.__make_parent_directories()

        with open(self.path, "w", encoding="utf-8") as page_file:
            json.dump(ipynb, page_file)

    def __refresh_path_name(self):
        self.path = self.path.with_name(self.__name)
        self.path = self.__join_name_count_if_exists()
        self.path = self.__join_path_extension_suffix()

    def __join_name_count_if_exists(self):
        name = self.path.name
        path = self.path.with_name(name)
        count = 0

        while path.with_suffix(path.suffix + ".ipynb").exists():
            count += 1
            name_count = " ".join([name, str(count)])
            path = self.path.with_name(name_count)

        return path

    def __join_path_extension_suffix(self):
        return self.path.with_suffix(self.path.suffix + ".ipynb")

    def __make_parent_directories(self):
        self.path.parent.mkdir(exist_ok=True, parents=True)
