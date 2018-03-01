#import sqlite3
import pymysql

class DB():
	ipaddr = None
	username = None
	password = None
	name = None
	conn = None
	
	def __init__(self, ipaddr, username, password, name):
		self.ipaddr = ipaddr
		self.username = username
		self.password = password
		self.name = name
		self.conn = pymysql.connect(ipaddr, username, password, name)
		return

	def connect(self):
		if not self.conn:
			self.conn = pymysql.connect(ipaddr, username, password, name)

	def get_cursor(self):
		if not self.conn:
			self.connect()
		return self.conn.cursor()

	def commit(self):
		self.conn.commit()

	def close(self):
		self.conn.close()
		return

class ForeignKey():
	refTable = None
	refField = None

	def __init__(self, table, field):
		self.refTable = table
		self.refField = field

	def to_sql(self):
		sql = 'REFERENCES {0}({1}) ON DELETE CASCADE ON UPDATE CASCADE'.format(self.refTable, self.refField)
		return sql

class Field():
	name = None
	recType = None
	required = None
	refTo = None
	parimary = None

	def __init__(self, name, recType, required, primary, refTo):
		self.name = name
		self.recType = recType
		self.required = required
		self.primary = primary
		self.refTo = refTo
	
	def to_str(self):
		sql = '{0} {1}'.format(self.name, self.recType)
		if self.primary:
			sql += ' PRIMARY KEY'
		if self.required:
			sql += ' NOT NULL'
		if self.name == 'id':
			sql += ' AUTO_INCREMENT'
		if self.refTo:
			sql += ', FOREIGN KEY({0}) {1}'.format(self.name, self.refTo.to_sql())
		return sql

class Table():
	name = None
	db = None
	schema = None
	pk = None

	def __init__(self, db, name, schema):
		self.name = name
		self.db = db
		self.schema = schema
		for s in self.schema:
			if s.primary:
				self.pk = s
		if not self.pk:
			self.pk = Field('id', 'INT', True, True, None)
			self.schema.append(self.pk)

	def get_rec_schema(self, recName):
		for s in self.schema:
			if s.name == recName:
				return s
		return None

	def create_table(self):
		c = self.db.get_cursor()

		sql = 'CREATE TABLE {0}('.format(self.name)
		for i in range(len(self.schema)):
			f = self.schema[i]
			sql += f.to_str()
			if i != len(self.schema) - 1:
				sql += ','
			else:
				sql += ')engine=innodb DEFAULT charset=utf8;'
		print(sql)

		c.execute('''{0}'''.format(sql))
		print('Table %s created successfully' % self.name)
		self.db.commit()
		return

	def drop_table(self):
		c = self.db.get_cursor()
		sql = '''DROP TABLE {0}'''.format(self.name)
		c.execute(sql)
		print("%s successfully" % sql)
		return

	def insert(self, vals):
		c = self.db.get_cursor()
		
		keySql = ''
		valSql = ''
		for i, item in enumerate(vals.items()):
			keySql += item[0]
			valSql += '\'' + str(item[1]) + '\''
			if i != len(vals) - 1:
				keySql += ', '
				valSql += ', '
		sql = "INSERT INTO {0}({1}) VALUES ({2})".format(self.name, keySql, valSql)

		try: 
			c.execute(sql)
			self.db.commit()
			print("%s successfully" % sql)
			return Reocrd(vals, self.schema)
		except:
			return None

	def row_to_record(self, row):
		vals = {}
		for i in range(len(self.schema)):
			fName = self.schema[i].name
			vals[fName] = row[i]
		return Record(vals, self.schema)

	def select_rec(self, field, value):
		c = self.db.get_cursor()

		retRecords = []
		sql = ''
		for i in range(len(self.schema)):
			fName = self.schema[i].name
			sql += fName
			if i != len(self.schema) - 1:
				sql += ','
		sql = 'SELECT {0} FROM {1} WHERE {2}=\'{3}\''.format(sql, self.name, field, value)
		print(sql)
		try:
			c.execute(sql)
			results = c.fetchall()
			for row in results:
				retRecords.append(self.row_to_record(row))
				print(retRecords[-1].to_str())
		except Exception as e:
			try:
				print('MySQL Error [%d]: %s' % (e.args[0], e.args[1]))
			except IndexError:
				print('MySQL Error: %s' % str(e))

		return retRecords

	def get_rec(self, key):
		recs = self.select_rec(self.pk.name, key)
		if len(recs) == 0:
			return None
		return recs[0]

class Record():
	vals = None
	fields = None

	def __init__(self, vals, fields):
		self.vals = vals
		self.fields = fields

	def get_val(self, field):
		return vals[field] 

	def to_str(self):
		return str(self.vals)

"""
def test_table(db, table, records, dump):
	pg = [{
		'gid' : 'ggg',
		'name' : 'gogogo'
	}, {
		'gid' : 'aaa',
		'name' : 'bbb'
	}]
	p = [{
		'pid' : 'pppp',
		'name' : 'nnnn',
		'alias' : 'alien',
		'gid' : 'ggg'
	}]
	f = [{
		'fid' : 'ffff',
		'image' : 'image.jpg',
		'pid' : 'pppp'
	}]
	e = [{
		'name' : 'eeee',
		'description' : 'This is test event',
		'timestamp' : 1519813150
	}]
	c = [{
		'timestamp' : 1519813150,
		'eid' : 1,
		'pid' : 'pppp'
	}]

	table.create_table()
	for rec in records:
		table.insert(rec)
	table.dump(dump[0], dump[1])

test_table(db, pgTable, pg, ('gid', 'ggg'))
test_table(db, pTable, p, ('pid', 'pppp'))
test_table(db, fTable, f, ('fid', 'ffff'))
test_table(db, eTable, e, ('id', 1))
test_table(db, cTable, c, ('id', 1))
		pg = [{
			'gid' : 'ggg',
			'name' : 'gogogo'
		}, {
			'gid' : 'aaa',
			'name' : 'bbb'
		}]
		for rec in pg:
			self.tables['PersonGroup'].insert(rec)
		self.tables['PersonGroup'].get_rec('ggg')


"""

