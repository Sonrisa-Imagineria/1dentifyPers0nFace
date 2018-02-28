import time
from database import DB
from database import Table
from database import ForeignKey
from database import Field

class ClockInDB():
	db = None
	tables = {
		'PersonGroup' : None,
		'Person' : None,
		'Face' : None,
		'Event' : None,
		'ClockIn' : None
	}

	def __init__(self, db):
		self.db = db
		self.init_tables()

	def clock_in(self, eid, pid):
		tables['ClockIn'].insert({
			'timestamp' : int(time.localtime()),
			'eid' : eid,
			'pid' : pid
		})
		return True
	
	def get_person_by_pid(self, pid):
		return tables['Person'].get_rec(pid)

	def drop_table(self, table):
		try:
			table.drop_table()
		except:
			print('no %s table' % table.name)

	def init_tables(self):
		db = self.db
		# person group table
		pgSchema = [Field('gid', 'CHAR(255)', True, True, None), 
					Field('name', 'TEXT', True, False, None), 
					Field('user_data', 'TEXT', False, False, None)]
		self.tables['PersonGroup'] = Table(db, 'PersonGroup', pgSchema)

		# person table
		pSchema =  [Field('pid', 'CHAR(255)', True, True, None), 
					Field('name', 'TEXT', True, False, None), 
					Field('alias', 'TEXT', True, False, None),
					Field('gid', 'CHAR(255)', True, False, ForeignKey(self.tables['PersonGroup'].name, 'gid'))]
		self.tables['Person'] = Table(db, 'Person', pSchema)

		# face table
		fSchema =  [Field('fid', 'CHAR(255)', True, True, None), 
					Field('image', 'TEXT', True, False, None), 
					Field('pid', 'CHAR(255)', True, False, ForeignKey(self.tables['Person'].name, 'pid'))]
		self.tables['Face'] = Table(db, 'Face', fSchema)

		# event table
		eSchema = [Field('name', 'TEXT', True, False, None), 
					Field('description', 'TEXT', True, False, None), 
					Field('timestamp', 'BIGINT', True, False, None)]
		self.tables['Event'] = Table(db, 'Event', eSchema)

		# clockin table
		cSchema =  [Field('timestamp', 'BIGINT', True, False, None), 
					Field('eid', 'INT', True, False, ForeignKey(self.tables['Event'].name, 'id')),
					Field('pid', 'CHAR(255)', True, False, ForeignKey(self.tables['Person'].name, 'pid'))]
		self.tables['ClockIn'] = Table(db, 'ClockIn', cSchema)

	def create_tables(self):
		self.drop_table(self.tables['ClockIn'])
		self.drop_table(self.tables['Event'])
		self.drop_table(self.tables['Face'])
		self.drop_table(self.tables['Person'])
		self.drop_table(self.tables['PersonGroup'])
		for i, table in enumerate(self.tables.items()):
			table[1].create_table()

	def close(self):
		db.close()

db = DB('localhost', 'test', '1234', 'testdb')
clkDB = ClockInDB(db)
clkDB.create_tables()
clkDB.close()

