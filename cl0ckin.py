# clockinsys.py
# coding=utf-8
import tkinter as tk
#import cognitive_face as CF
import cv2
import json
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
		ret = []
		for x in range(len(res)):
			ret.append({
				'faceId' : res[x]['faceId'],
				'personId' : res[x]['candidates'][0]['personId'],
				'confidence' : res[x]['candidates'][0]['confidence']
			})
		return ret

	def get_persons_from_image( self, image='caputre.jpg' ):
		face_res = self.faceAPI.detect_file(image)

		face_ids = []
		for face in face_res:
			face_ids.append(face['faceId'])
		persons_info = self.get_person_ids(face_ids)
		print(persons_info)
		for pinfo in persons_info:
			person = self.personAPI.get_person_info('yuhsiang', pinfo['personId'])
			print(pinfo['personId'])
			pinfo['name'] = person['name']
			pinfo['alias'] = person['userData']
			for face in face_res:
				if str(face['faceId']) == str(pinfo['faceId']):
					pinfo['faceRectangle'] = face['faceRectangle']
					break;


		print(json.dumps(persons_info))
		return persons_info

# fider = FaceIdentifier()
# fider.get_persons_from_image('test.jpg')
class ClockIn():
	video_capture = cv2.VideoCapture(0)
	font                   = cv2.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,250)
	fontScale              = 1
	fontColor              = (0,0,0)
	lineType               = 2
	persons_info = None

	def __init__(self):
		print( 'WIDTH',self.video_capture.get(3),'HEIGHT',self.video_capture.get(4))
		self.video_capture.set(3,640)
		self.video_capture.set(4,480)
	def start(self):
		while True:
			ret, frame = self.video_capture.read()
			if self.persons_info:
				cv2.putText(frame,'Hello World!',
			    self.bottomLeftCornerOfText,
			    self.font,
			    self.fontScale,
			    self.fontColor,
			    self.lineType)
			cv2.imshow('Company Meeting Check In Sys', frame)

			out = cv2.imwrite('capture.jpg', frame)

			if cv2.waitKey(1) & 0xFF == ord('q'):
#TODO periodical polling thread for get_person_info
clockrun = ClockIn()
clockrun.start()
