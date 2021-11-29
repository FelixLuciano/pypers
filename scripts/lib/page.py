from markdown import Markdown

from .config import *
from .style_parser import StyleParser


class Page():
    def __init__(self):
        self.filename = BASEDIR + "page.md"

        # Transform HTML
        md = Markdown(extensions=MARKDOWN_EXTENSIONS)
        with open(self.filename, "r", encoding="utf-8") as md_file:
            page_md = md_file.read()
        page = md.convert(page_md)

        # Extract metadata
        meta = {}
        for key, value in md.Meta.items():
            if len(value) == 1:
                meta[key] = value[0]
            elif JOIN_META:
                meta[key] = ", ".join(value)
            else:
                meta[key] = value

        # Apply styles
        styles = StyleParser()

        styles.add("pages/styles.json")
        styles.add(BASEDIR + "styles.json")
        styles.feed(page)

        self.page = styles.to_string()
        self.meta = meta


    def get_page(self, props={}):
        try:
            return self.page.format(**{
                **DATE,
                **CONFIG["props"],
                **self.meta,
                **props
            })

        except IndexError as error:
            raise Exception("Something went wrong while building!")
