import cv2
import numpy as np

# cap = cv2.VideoCapture(0)
hsvVals = [10, 100, 20, 25, 255, 255]
sensors = 3
threshold = 0.05
width, height = 480, 360
sensitivity = 3  # if number is high then sensitivity is low
weights = [-25, -15, 0, 15, 25]
fspeed = 15
curve = 0


def threshholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def getContours(imgThres, img):
    contours, hierarcy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(biggest)
    cx = x + w // 2
    cy = y + h // 2
    cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)
    return cx


def getSensorOutput(imgThres, sensors):
    imgs = np.hsplit(imgThres, sensors);                  # The number of splits that the image is split into
    totalpixels = img.shape[1] // sensors * img.shape[0]  #
    senOut = []
    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold * totalpixels:
            senOut.append(1)
        else:
            senOut.append(0)

        cv2.imshow(str(x), im)
    print(senOut)
    return senOut


def sendCommands(senOut, cx):
    global curve
    ## Translation :
    lr = (cx - width // 2) // sensitivity
    lr = int(np.clip(lr, -10, 10))

    if lr < 2 and lr > -2:
        lr = 0
    ## Rotation
    if senOut == [1, 0, 0]:
        curve = weights[0]
    elif senOut == [1, 1, 0]:
        curve = weights[1]
    elif senOut == [0, 1, 0]:
        curve = weights[2]
    elif senOut == [0, 1, 1]:
        curve = weights[3]
    elif senOut == [0, 0, 1]:
        curve = weights[4]

    elif senOut == [0, 0, 0]:
        curve = weights[2]
    elif senOut == [1, 1, 1]:
        curve = weights[2]
    elif senOut == [1, 0, 1]:
        curve = weights[2]

    # me.send_rc_control(lr,fspeed,0,curve)


# cap = cv2.VideoCapture(0)
url = "http://10.46.16.169:8080/video"       #DYNAMIC :uncomment for the dynamic test
cap = cv2.VideoCapture(url)                  #DYNAMIC :uncomment for the dynamic test
while True:
    _, img = cap.read()                      #DYNAMIC :uncomment for the dynamic test
    #### Testing on a static image
    # img = cv2.imread("Test_line_follower/Photo_orange.JPG")   #STATIC: Uncomment for the static test
    ####
    # cv2.imshow('image', img)
    img = cv2.resize(img, (width, height))

    # img_flip = img.flip(img,0)
    imgThres = threshholding(img)
    cx = getContours(imgThres, img)  # fo the drone to translate to the wanted x position
    senOut = getSensorOutput(imgThres, sensors)  # Rotation
    sendCommands(senOut, cx)
    cv2.imshow('image',img)
    cv2.imshow('path', imgThres)

    cv2.waitKey(100)
    print(img)



