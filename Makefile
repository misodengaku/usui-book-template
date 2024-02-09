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

pdf: $(BUILDDIR)/latex/output.pdf
	cp $(BUILDDIR)/latex/*.pdf output/

$(BUILDDIR)/latex/output.pdf: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work misodengaku/tex:$(SPHINXVER) make latexpdfja

open: $(BUILDDIR)/latex/output.pdf
	open $(BUILDDIR)/latex/output.pdf

latex: Makefile
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/$(BUILDDIR)/latex misodengaku/tex:$(SPHINXVER) platex -kanji=utf8 -recorder "output.tex"
	docker run -e PYTHONIOENCODING=utf-8 -it -v `pwd`:/work -w /work/$(BUILDDIR)/latex misodengaku/tex:$(SPHINXVER) dvipdfmx output.dvi

clean:
	rm -rf $(BUILDDIR)/*
