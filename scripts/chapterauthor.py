# encoding=utf-8

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util import texescape


class ChapterAuthorDirective(Directive):

    option_spec = {
        "author": directives.unchanged,
        "talker": directives.unchanged,
        "editor": directives.unchanged,
    }
    has_content = True

    def run(self):
        texescape.init()
        author = ""
        if "author" in self.options:
            author += "\\Large %s {[}著{]}\n\n" % texescape.escape(
                self.options["author"]
            )

        if "talker" in self.options:
            author += "\\Large %s {[}話{]}\n\n" % texescape.escape(
                self.options["talker"]
            )

        if "editor" in self.options:
            author += "%s {[}編{]}\n\n" % texescape.escape(self.options["editor"])

        source = """
{
\\begin{flushright}
%s
\\par\\nobreak\\vspace*{35pt}
\\end{flushright}
}
""" % (
            author
        )

        node = nodes.raw(source, source, format="latex")
        return [node]


class chapterauthor(nodes.Admonition, nodes.Element):
    pass


def visit_chapterauthor_node(self, node):
    self.visit_admonition(node)


def depart_chapterauthor_node(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(
        chapterauthor,
        latex=(visit_chapterauthor_node, depart_chapterauthor_node),
    )
    app.add_directive("chapterauthor", ChapterAuthorDirective)

    return {"version": "0.1"}  # identifies the version of our extension
