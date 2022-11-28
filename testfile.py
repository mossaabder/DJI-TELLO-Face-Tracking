import cv2
import numpy as np



w, h = 500, 360
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError_x = 0
pError_y = 0

def findFace(img):
    faceCascade  = cv2.CascadeClassifier("Ressource/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []
    myFaceListArea = []

    for (x,y,w,h)  in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0 , 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx,cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i= myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace( info, w, pid, pError_x, pError_y):
    up = 0
    area = info[1]
    x , y =  info[0]
    fb = 0
    error_x = x - w//2
    error_y = y - h//2
    speed_x = pid[0]*error_x + pid[1]*(error_x - pError_x)
    speed_x = int(np.clip(speed_x,-100,100))
    speed_y = pid[0] * error_y + pid[1] * (error_y - pError_y)
    speed_y = int(np.clip(speed_y, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    if area > fbRange[1]:
        fb = -20
    if area == 0:
        speed_x =0
        speed_y = 0
    elif area < fbRange[0] and area != 0:
        fb = 20

    print(speed_x,speed_y, fb)
    if x == 0:
        speed_x  = 0
        speed_y = 0
        error_x = 0
        error_y = 0

    me.send_rc_control(0, fb, speed_y, speed_x)

    return error_x, error_y

cap = cv2.VideoCapture(0)

while True:
    success, img1 = cap.read()
    img1 = cv2.resize(img1,(w ,h))
    img1, info1 = findFace(img1)
    pError = trackFace( info1, w, pid, pError_x, pError_y)
    # img = me.get_frame_read().frame
    # img = cv2.resize(img,(w ,h))
    # img, info = findFace(img)
    # pError = trackFace(me, info, w, pid, pError_x, pError_y)
    # print("Area", info[1])
    print("center_value", info1[0])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

