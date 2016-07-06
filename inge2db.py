#!/usr/bin/env python3

from shutil import copyfile
from uuid import uuid4
import sqlite3
import xlrd

rndfile = "/tmp/%s.db" % uuid4()
copyfile("./template.db", rndfile)

wb_filename = "filename.xls"

try:
	database = sqlite3.connect(rndfile)
	db_cur   = database.cursor()

	wb = xlrd.open_workbook(wb_filename, encoding_override='cp865')
	assert(wb.nsheets == 1)
	assert(wb.sheet_names() == ['Russere A5 papirer'])

	sh = wb.sheet_by_index(0)
	for rowX in range(sh.nrows):
		studyno    = sh.cell_value(rowX, 0)
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

except:
	print ("Unexpected error: %s" % sys.exc_info()[0])

# todos:
#	webpage (get wb_filename)
#	webpage (return rndfile)
#	Delete wb_filename
#	Delete rndfile
#	Log exceptions
