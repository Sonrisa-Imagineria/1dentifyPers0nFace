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

"""while True:
    ret, frame = video_capture.read()
    cv2.putText(frame,'Hello World!',
    bottomLeftCornerOfText,
    font,
    fontScale,
    fontColor,
    lineType)
    cv2.imshow('Company Meeting Check In Sys', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;
"""
# # KEY= 'e93923aa8c5642fdb09c54031087980a'
# # CF.Key.set(KEY)
# # url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
# # CF.BaseUrl.set(url)
# # img_url = 'https://imgur.com/a/8ezLR'
# # result = CF.face.detect(img_url)
# # print (result)
# #
# # # When everything is done, release the capture
# # video_capture.release()
# # cv2.destroyAllWindows()
# # win = tk.Tk()
# # win.title("WHO ARE YOU@Company Meeting")
# # win.mainloop()
# import face_recognition
# import cv2
#
# # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# # other example, but it includes some basic performance tweaks to make things run a lot faster:
# #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
# #   2. Only detect faces in every other frame of video.
#
# # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.
#
# # Get a reference to webcam #0 (the default one)
# video_capture = cv2.VideoCapture(0)
#
# # Load a sample picture and learn how to recognize it.
# # obama_image = face_recognition.load_image_file("obama.jpg")
# # obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
# #
# # # Load a second sample picture and learn how to recognize it.
# # biden_image = face_recognition.load_image_file("biden.jpg")
# # biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
#
# # Create arrays of known face encodings and their names
# # known_face_encodings = [
# #     obama_face_encoding,
# #     biden_face_encoding
# # ]
# # known_face_names = [
# #     "Barack Obama",
# #     "Joe Biden"
# # ]
#
# # Initialize some variables
# face_locations = []
# face_encodings = []
# face_names = []
# process_this_frame = True
#
# while True:
#     # Grab a single frame of video
#     ret, frame = video_capture.read()
#
#     # Resize frame of video to 1/4 size for faster face recognition processing
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#
#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     rgb_small_frame = small_frame[:, :, ::-1]
#
#     # Only process every other frame of video to save time
#     if process_this_frame:
#         # Find all the faces and face encodings in the current frame of video
#         face_locations = face_recognition.face_locations(rgb_small_frame)
#         face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
#
#         face_names = []
#         for face_encoding in face_encodings:
#             # See if the face is a match for the known face(s)
#             matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#             name = "Unknown"
#
#             # If a match was found in known_face_encodings, just use the first one.
#             if True in matches:
#                 first_match_index = matches.index(True)
#                 name = known_face_names[first_match_index]
#
#             face_names.append(name)
#
#     process_this_frame = not process_this_frame
#
#
#     # Display the results
#     for (top, right, bottom, left), name in zip(face_locations, face_names):
#         # Scale back up face locations since the frame we detected in was scaled to 1/4 size
#         top *= 4
#         right *= 4
#         bottom *= 4
#         left *= 4
#
#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#
#         # Draw a label with a name below the face
#         cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#         font = cv2.FONT_HERSHEY_DUPLEX
#         cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#
#     # Display the resulting image
#     cv2.imshow('Video', frame)
#
#     # Hit 'q' on the keyboard to quit!
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Release handle to the webcam
# video_capture.release()
# cv2.destroyAllWindows()
