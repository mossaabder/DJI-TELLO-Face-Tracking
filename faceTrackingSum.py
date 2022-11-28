import cv2
import numpy as np
from djitellopy import tello

#
# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamon()
#
# me.takeoff()


w, h = 720, 480
fbRange = [20000, 25000]
pid_x = [0.2, 0.2, 0]
pid_y = [0.2, 0.2, 0]
pError_x = 0
pError_y = 0
def findFace(img):
    faceCascade  = cv2.CascadeClassifier("Ressource/haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)

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
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]
def trackFace(me, info, w, h, pid_x, pid_y, pError_x, pError_y):
    up = 0
    area = info[1]
    x , y =  info[0]
    fb = 0
    """calcule de l'erreur en x et y"""
    error_x = x - w//2
    error_y = y - h//2
    """calcul la vitesse de commande PID pour l'ange de l'acet"""
    speed_x = pid_x[0]*error_x + pid_x[1]*(error_x - pError_x)
    speed_x = int(np.clip(speed_x,-100,100))
    '''calcul la vitesse de commande up and down'''
    speed_y = pid_y[0]*error_y + pid_y[1]*(error_y - pError_y)
    speed_y = int(np.clip(speed_y,-100,100))


    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    if area > fbRange[1]:
        fb = -20
    elif area < fbRange[0]:
        fb = 20

    if x == 0:
        speed_x = 0
        error_x = 0
    if y == 0:
        speed_y = 0
        error_y = 0
    print(speed_y)
    me.send_rc_control(0, fb, -speed_y, speed_x)

    return error_x, error_y
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    # img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError_x, pError_y = trackFace(me, info, w, h, pid_x, pid_y, pError_x, pError_y)
    # img = me.get_frame_read().frame
    # img = cv2.resize(img,(w ,h))
    # img, info = findFace(img)
    # pError_x, pError_y = trackFace(me, info, w, h, pid_x, pid_y, pError_x, pError_y)
    # print("Area", info[1])
    print("center_value", info[0])
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
