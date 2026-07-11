SPHINXVER     = 7.2.6
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean open pdf latex latexpdfja

latexpdfja: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

pdf: $(BUILDDIR)/latex/jiho_book.pdf
	cp $(BUILDDIR)/latex/jiho_book.pdf output/

$(BUILDDIR)/latex/jiho_book.pdf: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work misodengaku/tex:$(SPHINXVER) make latexpdfja

open: $(BUILDDIR)/latex/jiho_book.pdf
	open $(BUILDDIR)/latex/jiho_book.pdf

latex: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/$(BUILDDIR)/latex misodengaku/tex:$(SPHINXVER) platex -kanji=utf8 -recorder "jiho_book.tex"
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/$(BUILDDIR)/latex misodengaku/tex:$(SPHINXVER) dvipdfmx jiho_book.dvi

clean:
	rm -rf $(BUILDDIR)/*
