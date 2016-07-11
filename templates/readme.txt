This zip contains the following files:

 * [longname].db  - OLP.jar database
 * [longname].pdf - barcodes pdf
 * [longname].tex - barcodes LaTeX file
(* [longname].sqlite3 - "02350-Projekt" database)

This service is new. Expect bugs.

If you want to change in the barcodes, edit the .tex file
and recompile using XeLaTeX or run the following commands:
 * latex [longname].tex
 * dvips [longname].dvi
 * ps2pdf [longname].ps


For more info:
  https://github.com/NicolaiSoeborg/Inge2Beer
