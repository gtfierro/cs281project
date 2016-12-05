.SUFFIXES : .pdf .tex .zip

LATEX=pdflatex -synctex=1 -interaction=nonstopmode --shell-escape

FLAGS=-shell-escape

TEXFILES = $(wildcard *.tex ../*.tex)

PDF = main.pdf

pdf: $(PDF)

%.pdf: %.tex $(TEXFILES)
	rm -f *.aux *.out *.bbl *.blg *.toc
	pdflatex $(FLAGS) $*
	bibtex $*
	pdflatex $(FLAGS) $*
	pdflatex $(FLAGS) $*

opt: $(PDF)
	gs -q -dBATCH -dNOPAUSE -dSAFER -sDEVICE=pdfwrite \
	     -dPDFSETTINGS=/printer -dUseCIEColor -sOutputFile=out.pdf main.pdf
	mv out.pdf main.pdf

clean:
	rm -rf *~ *.log main.pdf *.aux *.out *.toc *.bbl *.blg
