import time
import os
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

	def set_person_group(self, gid, name, pid, data):
		return self.tables['PersonGroup'].insert({
			'gid' : gid,
			'name' : name,
			'pid' : pid,
			'user_data' : data
		})

	def get_person_group(self, gid):
		return self.tables['PersonGroup'].get_rec(gid)

	def set_person(self, pid, name, alias, gid):
		return self.tables['Person'].insert({
			'pid' : pid,
			'name' : name,
			'alias' : alias,
			'gid' : gid
		})

	def get_person(self, pid):
		return self.tables['Person'].get_rec(pid)

	def set_face(self, fid, image, pid):
		return self.tables['Face'].insert({
			'fid' : pid,
			'name' : name,
			'pid' : pid
		})

	def get_face(self, pid):
		return self.tables['Face'].get_rec(fid)

	def set_event(self, name, description):
		return self.tables['Event'].insert({
			'name' : name,
			'description' : description,
			'timestamp' : int(time.time())
		})

	def get_event(self, name):
		events = self.tables['Event'].select_rec('name', name)
		if len(events) != 0:
			return events[0]
		else:
			return None

	def set_clock_in(self, eid, pid):
		return self.tables['ClockIn'].insert({
			'timestamp' : int(time.time()),
			'eid' : eid,
			'pid' : pid
		})
	
	def get_clock_in(self, eid, pid):
		results = self.tables['ClockIn'].select_rec('pid', pid)
		for rec in results:
			if eid == rec.get_val(eid):
				return rec
		return None

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
		
		self.tables['PersonGroup'].create_table()
		self.tables['Person'].create_table()
		self.tables['Face'].create_table()
		self.tables['Event'].create_table()
		self.tables['ClockIn'].create_table()

	def close(self):
		db.close()

class ClockInDBBuilder():
	clkDB = None
	imageDir = None
	gid = 'gid-testgroup'
	groupName = 'testgroup'
	existingPerson = {}

	def __init__(self, clkDB, imageDir):
		self.clkDB = clkDB
		self.imageDir = imageDir

	def build(self):
		self.clkDB.create_tables()
		#self.build_person_group(gid, groupName, None)
		self.clkDB.close()
		return

	def build_person_group(self, gid, name, userData):
		# create person group with API
		personGroupAPI = PersonGroup()
		resp = personGroupAPI.train_person_group()
		# save into db
		self.clkDB.set_person_group(gid, name, userData)
		for dirpath, dirs, files in os.walk(self.imageDir):	
			for filename in files:
				imageName = os.path.splitext(filename)[0]
				alias = imageName
				# name = alias is ok ??? should be checked
				name = alias
				if "-" in imageName:
					alias = imageName[:imageName.find("-")]
				if alias not in existingPerson:
					# build person
					self.build_person(name, alias)
				# build face
				imagePath = os.path.join(self.imageDir, filename)
				self.build_face(imagePath, personId)
		return

	def build_person(self, name, alias):
		try:
			# create person with API
			personAPI = Person()
			resp = personAPI.create(gid, alias, alias)
			personId = resp['personId']
			# save into db
			personRec = self.clkDB.set_person(personId, alias, alias)
			exsitingPerson[alias] = personRec
		except:
			print("Error: failed to build person")
			personId = None

		return personId

	def build_face(self, imagePath, pid):
		try:
			# create face with person API
			personAPI = Person()
			resp = personAPI.add_a_face(gid, pid, imagePath)
			fid = resp['persistedFaceId']
			# save into db
			self.clkDB.set_face(fid, imagePath, pid)
		except:
			print("Error: failed to build face")
			fid = None
		return fid


db = DB('localhost', 'test', '1234', 'testdb')
clkDB = ClockInDB(db)
builder = ClockInDBBuilder(clkDB, 'image')

builder.build()

