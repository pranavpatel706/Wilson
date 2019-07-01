import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
kernel = np.ones((5, 5), np.uint8)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([5, 50, 143])
    upper_yellow = np.array([25, 249, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        area = cv2.contourArea(c)
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
        #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
        if area > 400:
            if len(approx)> 10:
                # calculate moments for each contour
                M = cv2.moments(c)
                # calculate x,y coordinate of center
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    cv2.putText(frame, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 3)
                    cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)


    # display the image
    cv2.imshow("frame", frame)
    key = cv2.waitKey(10)
    if key == 27:
       break
cap.release()
cv2.destroyAllWindows()