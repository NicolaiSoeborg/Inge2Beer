#!/usr/bin/env python3

from shutil import copyfile
import sys, os
import sqlite3
import xlrd

if len(sys.argv) != 2:
	print("Usage %s ruslist.xls" % sys.argv[0])
	exit(0)

wb_filename = sys.argv[1]
if not os.path.isfile(wb_filename):
	print("Can't find file '%s'." % wb_filename)
	exit(0)

db_olp_filename = "%s.db" % wb_filename
db_02350_filename = "%s.sqlite3" % wb_filename
if os.path.isfile(db_olp_filename) or os.path.isfile(db_02350_filename):
	print("Something went wrong!")
	exit(0)

homedir = os.path.dirname(sys.argv[0])
copyfile("%s/template.db" % homedir, db_olp_filename)
copyfile("%s/template.sqlite3" % homedir, db_02350_filename)

db_olp = sqlite3.connect(db_olp_filename)
db_02350 = sqlite3.connect(db_02350_filename)
db_olp_cur = db_olp.cursor()
db_02350_cur = db_olp.cursor()

wb = xlrd.open_workbook(wb_filename, encoding_override='cp1252')
assert(wb.nsheets == 1)
assert(wb.sheet_names() == ['Russere A5 papirer'])

barcodes = []

sh = wb.sheet_by_index(0)
for rowX in range(sh.nrows):
	studyno    = rowX
	try:
		studyno = int(sh.cell_value(rowX, 0))
	except ValueError:
		pass

	study      = "%s. %s" % (sh.cell_value(rowX, 1), sh.cell_value(rowX, 2))

	first_name = sh.cell_value(rowX, 5)
	last_name  = sh.cell_value(rowX, 6)
	name       = "%s %s" % (first_name, last_name)

	id         = rowX + 1
	barcode    = 1000 + rowX

	sql_olp = ("INSERT INTO USERS (ID, NAME, STUDYNUMBER, BARCODE, STUDY, TEAM,      RANK,  BEER, CIDER, SODA, COCOA, OTHER)"
	           " VALUES           (?,  ?,    ?,           ?,       ?,     'No Team', 'Rus', 0,    0,     0,    0,     0);")

	sql_02350 = ("INSERT INTO users (studentID, studentName, team,      rank)"
	             " VALUES           (?,         ?,           'No Team', 1);")


	db_olp_cur.execute(sql, (id, name, studyno, barcode, study))
	db_02350_cur.execute(sql, (barcode, name))

	barcodes.append((name, barcode))

db_olp.commit()
db_02350.commit()
db_olp.close()
db_02350.close()

pdf_header = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{fullpage,multicol}
\usepackage{pst-barcode}
\usepackage{framed}

\title{Inge2Beer: Barcodes}
\author{Nicolai Soeborg}
\date{July 2016}

\begin{document}
\begin{multicols}{3}"""

pdf_body = r"""\begin{framed}
NAME_TOKEN \\
\begin{pspicture}(0,-8pt)(1.5in,1in)
\psbarcode{BARCODE_TOKEN}{includetext width=1.6 height=1}{code39}
\end{pspicture}
\end{framed}"""

pdf_footer = r"""\end{multicols}
\end{document}"""

tex_filename = "%s.tex" % wb_filename
if os.path.isfile(tex_filename):
	print("Something went wrong!")
	exit(0)

with open(tex_filename, mode='w', encoding='utf-8') as f:
	f.write(pdf_header + "\n")
	for (name, barcode) in barcodes:
		f.write( pdf_body.replace("BARCODE_TOKEN", str(barcode)).replace("NAME_TOKEN", name) + "\n")
	f.write(pdf_footer)
