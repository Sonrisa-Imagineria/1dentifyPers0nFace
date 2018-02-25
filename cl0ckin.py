# clockinsys.py
# coding=utf-8
import tkinter as tk
import cognitive_face as CF

import cv2
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
