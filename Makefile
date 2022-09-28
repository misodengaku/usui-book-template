# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean open pdf latex latexpdfja

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
latexpdfja: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

pdf: build/latex/gps-ntp.pdf

build/latex/gps-ntp.pdf: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work misodengaku/tex make latexpdfja

open: build/latex/gps-ntp.pdf
	open build/latex/gps-ntp.pdf

latex: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/build/latex misodengaku/tex platex -kanji=utf8 -recorder "gps-ntp.tex"
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/build/latex misodengaku/tex dvipdfmx gps-ntp.dvi

clean:
	rm -rf build/*
