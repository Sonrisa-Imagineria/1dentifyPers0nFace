# clockinsys.py
# coding=utf-8
import tkinter as tk
#import cognitive_face as CF
import cv2
import json
import _thread
import time
import queue as Queue
import numpy as np
from webapi import MSFaceAPI
from webapi import Face
from webapi import PersonGroup
from webapi import Person
from database import DB
from database import Table
from database import ForeignKey
from database import Field
from db_cl0ckin import ClockInDB
from db_cl0ckin import ClockInDB

class FaceIdentifier():
	personGroupId = ''
	faceAPI = Face()
	personAPI = Person()

	def __init__(self, person_group_id='yuhsiang'):
		self.personGroupId = person_group_id

	def get_person_ids( self, face_ids ):
		res = self.faceAPI.identify(face_ids, self.personGroupId)
		print(res)
		ret = []
		for x in range(len(res)):
			ret.append({
				'faceId' : res[x]['faceId'],
				'personId' : res[x]['candidates'][0]['personId'],
				'confidence' : res[x]['candidates'][0]['confidence']
			})
		return ret

	def get_persons_from_image( self, image, out_queue ):
		face_res = self.faceAPI.detect_file(image)

		face_ids = []
		for face in face_res:
			if type(face)==type({}):
				face_ids.append(face['faceId'])
		if len(face_ids)==0:
			return None
		persons_info = self.get_person_ids(face_ids)

		for pinfo in persons_info:
			person = self.personAPI.get_person_info('yuhsiang', pinfo['personId'])
			pinfo['name'] = person['name']
			pinfo['alias'] = person['userData']
			for face in face_res:
				if str(face['faceId']) == str(pinfo['faceId']):
					pinfo['faceRectangle'] = face['faceRectangle']
					break;

		#print(json.dumps(persons_info))
		out_queue.put(persons_info)
		return persons_info

	def get_persons_from_image_async( self, image, persons_info_queue ):
		try:
			_thread.start_new_thread( self.get_persons_from_image, (image, persons_info_queue ) )
		except:
			print ("Error: cannot start thread")

# fider = FaceIdentifier()
# fider.get_persons_from_image('test.jpg')

class ClockIn():
	video_capture = cv2.VideoCapture(0)
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,250)
	fontScale              = 1
	fontColor              = (0,0,0)
	lineType               = 2
	persons_info_queue = Queue.Queue()
	fider = FaceIdentifier()
	last_update_persons_info_time = 0
	update_period = 1
	clkDB = None
	event = None

	def __init__(self, db):
		print( 'WIDTH',self.video_capture.get(3),'HEIGHT',self.video_capture.get(4))
		self.video_capture.set(3,640)
		self.video_capture.set(4,480)
		self.clkDB = ClockInDB(db)

	def init_event(self, name, desc):
		self.event = self.clkDB.get_event(name)
		if not self.event:
			self.clkDB.set_event(name, desc)
			self.event = self.clkDB.get_event(name)
		return self.event

	def clock_in(self, pid):
		if not self.clkDB.get_person(pid):
			return None
		self.clkDB.set_clock_in(self.event.vals['id'], pid)
		return self.is_clocked(pid)

	def is_clocked(self, pid):
		return self.clkDB.get_clock_in(self.event.vals['id'], pid)

	def get_persons_info_from_queue(self):
		try:
			persons_info = self.persons_info_queue.get(False)
			return persons_info
		except:
			return None
	def put_position(self, left, height):
		text_position = (left,height)
		return text_position
	def add_frame(self, frame, leftTop, rightBottom, color):
		img = np.zeros((512,512,3), np.uint8)
		cv2.rectangle(frame, leftTop, rightBottom, color, 5)
	def add_name_tag(self, frame, per_info):
		name = per_info['name']
		clocked = self.is_clocked(per_info['personId'])
		leftTop = (per_info['faceRectangle']['left'], per_info['faceRectangle']['top'])
		rightBottom = (per_info['faceRectangle']['left'] + per_info['faceRectangle']['width'],
						per_info['faceRectangle']['top'] + per_info['faceRectangle']['height'])
		if clocked:
			color = (55, 255, 155)
			cv2.putText(frame, name, leftTop, self.font, self.fontScale, self.fontColor, self.lineType)
		else:
			color = (255, 0, 0)
		self.add_frame(frame, leftTop, rightBottom, color)
	def start(self):
		info=None
		while True:
			ret, frame = self.video_capture.read()

			current_time = time.time()
			if (current_time - self.last_update_persons_info_time) > self.update_period:
				out = cv2.imwrite('capture.jpg', frame)
				self.fider.get_persons_from_image_async('capture.jpg', self.persons_info_queue)
				self.last_update_persons_info_time = current_time
				info = self.get_persons_info_from_queue()
				"""if tmp_info:
					print('tmp-info///yes!')
					print(tmp_info)
					info = tmp_info """
			if info:
				for x in range(0, len(info)):
					if info[x]['confidence'] > 0.7:
						self.clock_in(info[x]['personId'])
						self.add_name_tag(frame, info[x])
					#else:
					#	self.add_warning_frame(frame,info[x])
					#	self.alert_view()

			cv2.imshow('Company Meeting Check In Sys', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break;

class AlertView():
	root = None
	frame = None
	label = None 
	text_field = None
	button = None
	
	def __init__(self, callback):
		self.root = tk.Tk()
		self.frame = tk.Frame(self.root, bg='white')
		self.label = tk.Label(self.frame, text="Alias",bg='white') 
		self.text_field = tk.Text(self.frame, height=1, width=20)
		self.button = tk.Button(self.frame, text="Submit", bg='gray', height=1, command=lambda: self.onclick(callback))

	def onclick(self, callback):
		content = self.text_field.get("1.0", "end-1c")
		callback(content)

	def show(self):
		# optionally give it a title
		self.root.title("Q3 Company Meeting")
		# set the root window's height, width and x,y position
		# x and y are the coordinates of the upper left corner
		w = 300
		h = 100
		x = 50
		y = 100
		# use width x height + x_offset + y_offset (no spaces!)
		self.root.geometry("%dx%d+%d+%d" % (w, h, x, y))
		# use a colorful frame
		self.frame.pack(fill='both', expand='yes')
		# position a label on the frame using place(x, y)
		# place(x=0, y=0) would be the upper left frame corner
		self.label.place(x=20, y=30)
		# put the button below the label, change y coordinate
		self.text_field.place(x=60,y=30)

		self.button.place(x=230, y=27)

		self.root.mainloop()

db = DB('localhost', 'test', '1234', 'testdb')
clk = ClockIn(db)
clk.clkDB.create_tables()
clk.clkDB.set_person_group('ggg', 'groupname', 'data')
clk.clkDB.set_person('ppp', 'name', 'alias', 'ggg')
clk.init_event('test_event', 'descc')
clk.clock_in('ppp')
if clk.is_clocked('ppp'):
	print('ppp clockin!')
if not clk.is_clocked('aaa'):
	print('aaa not clockin!')
#clk.start()
alert = AlertView(clk.clock_in)
alert.show()
