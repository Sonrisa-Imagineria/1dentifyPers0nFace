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

	def __init__(self):
		print( 'WIDTH',self.video_capture.get(3),'HEIGHT',self.video_capture.get(4))
		self.video_capture.set(3,640)
		self.video_capture.set(4,480)

	def get_persons_info_from_queue(self):
		try:
			persons_info = self.persons_info_queue.get(False)
			return persons_info
		except:
			return None
	def put_position(self, left, height):
		text_position = (left,height)
		return text_position
	def add_name_tag(self, frame, per_info):
		name = per_info['name']
		leftTop = (per_info['faceRectangle']['left'], per_info['faceRectangle']['top'])
		rightBottom = (per_info['faceRectangle']['left'] + per_info['faceRectangle']['width'],
						per_info['faceRectangle']['top'] + per_info['faceRectangle']['height'])
		img = np.zeros((512,512,3), np.uint8)
		# print(name)
		cv2.rectangle(frame, leftTop, rightBottom, (55, 255, 155), 5)
		cv2.putText(frame, name, leftTop, self.font, self.fontScale, self.fontColor, self.lineType)
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
			# print(persons_info)
			if info:
				# print(len(info))
				for x in range(0, len(info)):
					self.add_name_tag(frame, info[x])
    			# 	print "We're on time %d" % (x)
				# cv2.putText(frame,info[0]['name'], self.bottomLeftCornerOfText, self.font, self.fontScale, self.fontColor, self.lineType)

			cv2.imshow('Company Meeting Check In Sys', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break;

clk = ClockIn()
clk.start()
