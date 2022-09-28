#encoding=utf-8

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import texescape
import shutil

class WideFigureDirective(Directive):

    has_content = True

    def run(self):
        filepath = self.content[0]
        caption = self.content[2]
        filename = filepath.split("/")[-1]
        shutil.copyfile("./source/" + filepath, "./build/latex/" + filename)

        texescape.init()
        source = u"""
\\begin{figure*}[htbp]
\\centering
\\capstart

\\noindent\\sphinxincludegraphics{%s}
\\caption{%s}\end{figure*}
""" % (filename, texescape.escape(caption))

        node = nodes.raw(source, source, format="latex")
        return [node]

class widefigure(nodes.Admonition, nodes.Element):
    pass

def visit_widefigure_node(self, node):
    self.visit_admonition(node)

def depart_widefigure_node(self, node):
    self.depart_admonition(node)

def setup(app):
    app.add_node(widefigure, latex=(visit_widefigure_node, depart_widefigure_node), )
    app.add_directive('widefigure', WideFigureDirective)

    return {'version': '0.1'}   # identifies the version of our extension
