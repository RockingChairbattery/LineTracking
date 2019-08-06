import cv2
import numpy as np

frame = cv2.imread('/Users/rockingchairbattery/Desktop/2019a glasgow/tdps/sample/1.png')
x, y = frame.shape[0:2]
frame = cv2.resize(frame, (0, 0), fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
frame = gaussianflter
cv2.imshow("frame", frame)
hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)


def on_hsv():
    low_h = cv2.getTrackbarPos("LOW_H", "CONTROL")
    high_h = cv2.getTrackbarPos("HIGH_H", "CONTROL")
    low_s = cv2.getTrackbarPos("LOW_s", "CONTROL")
    high_s = cv2.getTrackbarPos("HIGH_s", "CONTROL")
    low_v = cv2.getTrackbarPos("LOW_v", "CONTROL")
    high_v = cv2.getTrackbarPos("HIGH_v", "CONTROL")
    lower_hsv = np.array([low_h, low_s, low_v])
    upper_hsv = np.array([high_h, high_s, high_v])
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    cv2.imshow("hsv", mask)


cv2.namedWindow("CONTROL")
cv2.createTrackbar("LOW_H", "CONTROL", 0, 255, on_hsv)
cv2.createTrackbar("HIGH_H", "CONTROL", 0, 255, on_hsv)
cv2.createTrackbar("LOW_s", "CONTROL", 0, 255, on_hsv)
cv2.createTrackbar("HIGH_s", "CONTROL", 0, 255, on_hsv)
cv2.createTrackbar("LOW_v", "CONTROL", 0, 255, on_hsv)
cv2.createTrackbar("HIGH_v", "CONTROL", 0, 255, on_hsv)


while 1:
    on_hsv()

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()

