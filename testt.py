import cv2

while True:
    cap = cv2.VideoCapture(0)
    something_i, img = cap.read()
    img = cv2.resize(img, (480,360))
    cv2.imshow('image',img)
    cv2.waitKey(100)