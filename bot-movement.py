import RPi.GPIO as gpio
from time import sleep

#pin 17 left wheels +
# pin 22 left wheels -
#pin 23 right wheels +
# pin 24 right wheels -
# pin 18 rotor +
# pin 15 rotor -

gpio.setmode(gpio.BOARD)
gpio.setup(17, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(18, gpio.OUT)
gpio.setup(15, gpio.OUT)

def forward(t):
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    sleep(t)

def rright(t):
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    sleep(t)

def rleft(t):
    gpio.output(17, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    sleep(t)