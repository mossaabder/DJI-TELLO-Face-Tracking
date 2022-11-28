import cv2
import numpy as np
url = "http://10.46.16.169:8080/video"
cap = cv2.VideoCapture(url)
while True:
    camera, frame = cap.read()
    image = cv2.resize(frame, (480, 360))
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_filt = cv2.inRange(image_hsv,(10,100,20),(25,255,255))
    cv2.imshow('image',image_filt)
    # frame = cv2.resize(frame,(480,360))
    if frame is not None:
        cv2.imshow("Frame", image_filt)
    q = cv2.waitKey(1)
    # if q==ord("q"):
    #     break
cv2.destroyAllWindows()