import RPi.GPIO as gpio
from time import sleep
import cv2
import numpy as np
from math import cos, radians

# pin 17 left wheels +
# pin 22 left wheels -
# pin 23 right wheels +
# pin 24 right wheels -
# pin 18 rotor +
# pin 15 rotor -

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(15, gpio.OUT)


def distance(cY):

def theta(cX,cY):


def Stopall():
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)


def forward(t):
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    sleep(t)
    Stopall()


def rright(t):
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    sleep(t)
    Stopall()


def rleft(t):
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    sleep(t)
    Stopall()


def backward(t):
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    sleep(t)
    Stopall()


cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
kernel = np.ones((10, 10), np.uint8)
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([27, 109, 46])
    upper_green = np.array([47, 255, 229])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    _, contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dist = 300.0
    t = 180.0
    for c in contours:
        area = cv2.contourArea(c)
        radius = (area / 3.14) ** 0.5
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        # cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
        if area > 5:
            if 8 < len(approx):
                # calculate moments for each contour
                M = cv2.moments(c)
                # calculate x,y coordinate of center
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    d = distance(cY) / cos( radians(theta(cX,cY)))
                    if d <= dist:
                        dist = d
                        t = theta(cX,cY)
                    # cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    # cv2.putText(frame, "centroid" , (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 3)
                    # cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
    if dist == 300.0 and t = 180.0 :
        rright()
    else:
        if t > 0:
            rright()
            forward()
        else:
            rleft()
            forward()


    # display the image
    cv2.imshow("frame", frame)
    cv2.imshow("openong", opening)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()