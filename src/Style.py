import cssutils


class Style:
    @staticmethod
    def apply_styleSheet(tree, stylesheet):
        for rule in stylesheet:
            if isinstance(rule, cssutils.css.CSSImportRule):
                Style.apply_styleSheet(tree, rule.styleSheet)

            elif isinstance(rule, cssutils.css.CSSStyleRule):
                Style.__apply_stylesheet_declarations(tree, rule)

    @staticmethod
    def __apply_stylesheet_declarations(tree, rule):
        for node in tree.select(rule.selectorText):
            Style.__apply_node_stylesheet_declarations(node, rule)

    @staticmethod
    def __apply_node_stylesheet_declarations(node, rules):
        style = Style.__get_node_style_declarations(node)

        for declaration in rules.style:
            Style.__apply_style_declaration(style, declaration)

        node["style"] = style.cssText

    @staticmethod
    def __get_node_style_declarations(node):
        if not node.has_attr("style"):
            node["style"] = ""

        return cssutils.css.CSSStyleDeclaration(node["style"])

    def __apply_style_declaration(style, declaration):
        style.removeProperty(declaration.name)
        style.setProperty(declaration.name, declaration.value)
