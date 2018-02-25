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

		for pinfo in persons_info:
			person = self.personAPI.get_person_info('yuhsiang', pinfo['personId'])
			pinfo['name'] = person['name']
			pinfo['alias'] = person['userData']
			for face in face_res:
				if str(face['faceId']) == str(pinfo['faceId']):
					pinfo['faceRectangle'] = face['faceRectangle']
					break;

		
		print(json.dumps(persons_info))
		return persons_info

#fider = FaceIdentifier()
#fider.get_persons_from_image('test.jpg')

video_capture = cv2.VideoCapture(0)
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,250)
fontScale              = 1
fontColor              = (0,0,0)
lineType               = 2
print( 'WIDTH',video_capture.get(3),'HEIGHT',video_capture.get(4))

video_capture.set(3,640)
video_capture.set(4,480)

while True:
    ret, frame = video_capture.read()
    cv2.putText(frame,'Hello World!',
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)
    cv2.imshow('Company Meeting Check In Sys', frame)

    out = cv2.imwrite('capture.jpg', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
