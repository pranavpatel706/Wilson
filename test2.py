import cv2
import numpy as np
from math import exp
import RPi.GPIO as gpio
from time import sleep
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
    dist = (1214*exp(-0.03288*cY))+(148.1*exp(-0.005278*cY))
    return dist
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


i=0
j=0
w = 1200.0
speed = 51.0
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
kernel = np.ones((8, 8), np.uint8)
CcX = 650
CcY = 490
while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([39, 41, 64])
    upper_green = np.array([68, 235, 203])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    _, contours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dist = 300.0
    for c in contours:
        area = cv2.contourArea(c)
        radius = (area/3.14)**0.5
        approx = cv2.approxPolyDP(c, 0.01*cv2.arcLength(c, True), True)
        #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
        if area > 100:
            if 5 < len(approx) :
                # calculate moments for each contour
                M = cv2.moments(c)
                # calculate x,y coordinate of center
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
                    cv2.putText(frame, "centroid" , (cX - 25, cY - 25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 3)
                    d = distance(cY)
                    if d is not None:
                        if d < dist:
                            dist = d
                            CcX = cX
                            CcY = cY
                    #cv2.drawContours(frame, [approx], 0, (0, 0, 0), 5)
    print(dist ,CcX, CcY)
    if dist == 300.0 and  CcX == 650 :
            i = i + 1
            print("shit")

    else:
        print("1")
        i = 0
        j = 0
        if CcX < 310:
            print("2")
            time =  float((310 - CcX)) /w
            rleft(time)

        elif CcX > 330:
            print("3")
            time = float((CcX - 330)) /w
            rright(time)
        else:
            print("4")
            time = dist /speed
            forward(time)



    if i == 5000:
        rright(0.5)
        j = j + 1

    
    # display the image
    cv2.imshow("frame", frame)
    cv2.imshow("openong", opening)
    key = cv2.waitKey(1)
    if key == 27:
       break
cap.release()
cv2.destroyAllWindows()