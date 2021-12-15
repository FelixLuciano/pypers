from markdown import Markdown

from .config import *
from .style_parser import StyleParser
from .props import load_props


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


        # Load computed props
        props = load_props("pages/props.py")
        props.update(load_props(BASEDIR + "props.py"))

        # Apply styles
        styles = StyleParser()

        styles.add("pages/styles.json")
        styles.add(BASEDIR + "styles.json")
        styles.feed(page)

        self.page  = styles.to_string()
        self.meta  = meta
        self.props = props


    def get_page(self, props={}):
        props = {
            **CONFIG["props"],
            **self.props,
            **self.meta,
            **props
        }

        if "update" in self.props:
            updated = self.props["update"](props.copy())

            if updated is not None:
                props.update(updated)

        try:
            return self.page.format(**props)
        except IndexError as error:
            raise Exception("Something went wrong while building!")
