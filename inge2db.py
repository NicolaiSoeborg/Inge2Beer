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

newfile = "%s.db" % wb_filename.replace(".xls", "")
if os.path.isfile(newfile):
	print("Something went wrong!")
	exit(0)

copyfile("./template.db", newfile)

database = sqlite3.connect(newfile)
db_cur   = database.cursor()

wb = xlrd.open_workbook(wb_filename, encoding_override='cp865')
assert(wb.nsheets == 1)
assert(wb.sheet_names() == ['Russere A5 papirer'])

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

	sql = ("INSERT INTO USERS (ID, NAME, STUDYNUMBER, BARCODE, STUDY, TEAM,      RANK,  BEER, CIDER, SODA, COCOA, OTHER)"
	       " VALUES           (?,  ?,    ?,           ?,       ?,     'No Team', 'Rus', 0,    0,     0,    0,     0);")

	db_cur.execute(sql, (id, name, studyno, barcode, study))

database.commit()
database.close()

os.remove(wb_filename) # delete workbook
