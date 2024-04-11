# encoding=utf-8

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util import texescape
import shutil


class CustomFigureDirective(Directive):

    option_spec = {
        "position": directives.unchanged,
        "caption": directives.unchanged,
        "clearpage": directives.flag,
    }
    has_content = True

    def run(self):
        filepath = self.content[0]
        caption = ""
        if "caption" in self.options:
            caption = self.options["caption"]
        filename = filepath.split("/")[-1]
        position = "htbp"
        if "position" in self.options:
            position = self.options["position"]
        shutil.copyfile("./source/" + filepath, "./build/latex/" + filename)

        texescape.init()
        source = """
\\begin{figure}[%s]
\\centering
\\capstart
\\noindent\\sphinxincludegraphics{%s}
\\caption{%s}
\\end{figure}
""" % (
            position,
            filename,
            texescape.escape(caption),
        )
        if "clearpage" in self.options and self.options["clearpage"]:
            source += "\\clearpage"

        node = nodes.raw(source, source, format="latex")
        return [node]


class customfigure(nodes.Admonition, nodes.Element):
    pass


def visit_customfigure_node(self, node):
    self.visit_admonition(node)


def depart_customfigure_node(self, node):
    self.depart_admonition(node)


def setup(app):
    app.add_node(
        customfigure,
        latex=(visit_customfigure_node, depart_customfigure_node),
    )
    app.add_directive("customfigure", CustomFigureDirective)

    return {"version": "0.1"}  # identifies the version of our extension
