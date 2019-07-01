import cv2
import numpy as np

def nothing(x):
    pass

cap = cv2.VideoCapture(-1)
cv2.namedWindow("tracking")
cv2.createTrackbar("lh", "tracking", 0, 255,nothing)
cv2.createTrackbar("ls", "tracking", 0, 255,nothing)
cv2.createTrackbar("lv", "tracking", 0, 255,nothing)
cv2.createTrackbar("uh", "tracking", 255, 255,nothing)
cv2.createTrackbar("us", "tracking", 255, 255,nothing)
cv2.createTrackbar("uv", "tracking", 255, 255,nothing)
kernel = np.ones((5, 5), np.uint8)

while True:
      _, frame = cap.read()
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      lh = cv2.getTrackbarPos("lh", "tracking")
      ls = cv2.getTrackbarPos("ls", "tracking")
      lv = cv2.getTrackbarPos("lv", "tracking")
      uh = cv2.getTrackbarPos("uh", "tracking")
      us = cv2.getTrackbarPos("us", "tracking")
      uv = cv2.getTrackbarPos("uv", "tracking")

      l_b = np.array([lh, ls, lv])
      u_b = np.array([uh, us, uv])

      mask = cv2.inRange(hsv,l_b,u_b)
      opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

      contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

      #for cnt in contours:
           # cv2.drawContours(frame, [cnt], 0, (0,0,0),5)
      res = cv2.bitwise_and(frame,frame,mask=mask)

      cv2.imshow("frame", frame)
      cv2.imshow("mask", mask)
      cv2.imshow("res", res)

      key = cv2.waitKey(1)
      if key == 27:
          break
cap.release()
cv2.destroyAllWindows()