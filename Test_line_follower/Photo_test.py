import cv2



while True:
    image = cv2.imread("Photo_orange.JPG")
    image = cv2.resize(image, (480, 360))
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_filt = cv2.inRange(image_hsv,(10,100,20),(25,255,255))
    cv2.imshow('image',image_filt)
    cv2.waitKey(10)







