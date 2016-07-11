This zip contains the following files:

 * Barcodes.pdf - barcodes pdf
 * Barcodes.tex - barcodes LaTeX file
 * Beer.db  - OLP.jar database
(* TEST-02350.sqlite3 - "02350-Projekt" database)

This service is new. Expect bugs.

If you want to change in the barcodes, edit the .tex file
and recompile using XeLaTeX or run the following commands:
 * latex Barcodes.tex
 * dvips Barcodes.dvi
 * ps2pdf Barcodes.ps

You'll need the `pst-barcode` and `pstricks` package for LaTeX.

For more info:
  https://github.com/NicolaiSoeborg/Inge2Beer
