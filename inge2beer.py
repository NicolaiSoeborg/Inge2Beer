#!/usr/bin/env python3

from shutil import copyfile
import sys, os
import sqlite3
import xlrd
import random, string # for gen seeds

if len(sys.argv) != 2:
	sys.exit("Usage %s ruslist.xls" % sys.argv[0])

wb_filename = sys.argv[1]
if not os.path.isfile(wb_filename):
	sys.exit("Can't find file '%s'." % wb_filename)

dbs = { 'OLP':   {'file': "%s.db" % wb_filename},
	'02350': {'file': "%s.sqlite3" % wb_filename}}
for db in dbs:
	if os.path.isfile(dbs[db]['file']):
		sys.exit("Error '%s' already exists!" % dbs[db]['file'])

homedir = os.path.dirname(sys.argv[0]) or "."
copyfile("%s/templates/OLP.db" % homedir, dbs['OLP']['file'])
copyfile("%s/templates/02350.sqlite3" % homedir, dbs['02350']['file'])

dbs['OLP']['db'] = sqlite3.connect(dbs['OLP']['file'])
dbs['OLP']['cur'] = dbs['OLP']['db'].cursor()
dbs['02350']['db'] = sqlite3.connect(dbs['02350']['file'])
dbs['02350']['cur'] = dbs['02350']['db'].cursor()

try:
	wb = xlrd.open_workbook(wb_filename, encoding_override='cp1252')
except xlrd.biffh.XLRDError:
	wb = xlrd.open_workbook("sample.xls", encoding_override='cp1252')
assert(wb.nsheets == 1)
assert(wb.sheet_names() == ['Russere A5 papirer'])

barcodes = []

sh = wb.sheet_by_index(0) # sheet_by_name("Russere A5 papirer")
for rowX in range(sh.nrows): # todo: catch IndexError
	try:
		studyno = int(sh.cell_value(rowX, 0))
	except ValueError:
		studyno = rowX

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


	dbs['OLP']['cur'].execute(sql_olp, (id, name, studyno, barcode, study))
	dbs['02350']['cur'].execute(sql_02350, (str(barcode), name))

	barcodes.append((name, barcode))

dbs['OLP']['db'].commit()
dbs['OLP']['db'].close()
dbs['02350']['db'].commit()
dbs['02350']['db'].close()


pdf_header = r"""\documentclass{article}
\usepackage{ifxetex}
\ifxetex
   \usepackage{fontspec}
\else
   \usepackage[utf8]{inputenc}
\fi
\usepackage{fullpage,multicol}
\usepackage{pst-barcode,framed}

\title{Inge2Beer: Barcodes}
\author{Nicolai Søborg}
\date{July 2016}

\begin{document}
\begin{multicols}{3}"""

seed = ''.join(random.choice(string.ascii_letters) for _ in range(32))
pdf_body = r"""\begin{framed}
\centering
NAME_TOKEN \\
\begin{pspicture}(0,-8pt)(1.5in,1in)
\psbarcode{BARCODE_TOKEN}{includetext width=1.6 height=1}{code39}
\end{pspicture}
\end{framed}""".replace("NAME_TOKEN", seed)

pdf_footer = r"""\end{multicols}
\end{document}"""

tex_filename = "%s.tex" % wb_filename
if os.path.isfile(tex_filename):
	sys.exit("Error: File '%s' already exists!" % tex_filename)

with open(tex_filename, mode='w', encoding='utf-8') as f:
	f.write(pdf_header + "\n")
	for i, (name, barcode) in enumerate(barcodes):
		body = pdf_body.replace("BARCODE_TOKEN", str(barcode))
		body     = body.replace(seed, name.replace("\\", ""))
		if i > 0 and i % 14 == 0:
			body += "\n\clearpage" # try to fix LaTeX floats handling ...
		f.write( body + "\n")
	f.write(pdf_footer)
