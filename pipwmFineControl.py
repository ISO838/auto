#Import libraries
import sys
import time
from time import sleep
import RPi.GPIO as GPIO

#Set the GPIO pin configurations
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


#Define the output pins
my_pwmForwards=GPIO.PWM(26,100)
my_pwmBackwards=GPIO.PWM(20,100)
my_pwmRight=GPIO.PWM(16,20)
my_pwmLeft=GPIO.PWM(19,20)

#Start the PWM process with 0 duty cycle
my_pwmRight.start(0)
my_pwmLeft.start(0)
my_pwmForwards.start(0)
my_pwmBackwards.start(0)

# Motor functions:

def moveForwards(): #Move the main drive motor forwards
        my_pwmForwards.ChangeDutyCycle(35)
        sleep(5)
        my_pwmForwards.ChangeDutyCycle(0)

def moveBackwards(): #Move the main drive motor backwards
        my_pwmBackwards.ChangeDutyCycle(35)
        sleep(5)
        my_pwmBackwards.ChangeDutyCycle(0)

def moveRight(): #Move the turning motor right
        my_pwmRight.ChangeDutyCycle(15)
        sleep(1)
        my_pwmRight.ChangeDutyCycle(0)


def moveLeft(): #Move the turning motor left
        my_pwmLeft.ChangeDutyCycle(15)
        sleep(1)
        my_pwmLeft.ChangeDutyCycle(0)


#Begin the program:
moveRight()
moveForwards()
sleep(1)
moveBackwards()
moveLeft()

#Clean up the GPIO pins to avoid errors on next run:

GPIO.cleanup()