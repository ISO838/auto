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

#Define the output pins and PWM frequency
pwmForwards=GPIO.PWM(26,100)
pwmBackwards=GPIO.PWM(20,100)
pwmRight=GPIO.PWM(16,1)
pwmLeft=GPIO.PWM(19,1)

#Start the PWM process with 0 duty cycle
pwmRight.start(0)
pwmLeft.start(0)
pwmForwards.start(0)
pwmBackwards.start(0)

# Motor functions:
def moveForwards(): #Move the main drive motor forwards
        pwmForwards.ChangeDutyCycle(50)
        print"Move forwards"
        sleep(5)
        pwmForwards.ChangeDutyCycle(0)
def moveBackwards(): #Move the main drive motor backwards
        pwmBackwards.ChangeDutyCycle(50)
        print"Move backwards"
        sleep(5)
        pwmBackwards.ChangeDutyCycle(0)
def moveRight(): #Move the turning motor right
        pwmRight.ChangeDutyCycle(15)
        print"Move right"
        sleep(1)
        pwmRight.ChangeDutyCycle(0)
def moveLeft(): #Move the turning motor left
        pwmLeft.ChangeDutyCycle(15)
        print"Move left"
        sleep(1)
        pwmLeft.ChangeDutyCycle(0)
def driveRight(): #Drive forwards and turn right
        pwmForwards.ChangeDutyCycle(40)
        pwmRight.ChangeDutyCycle(15)
        sleep(1)
        pwmForwards.ChangeDutyCycle(0)
        pwmRight.ChangeDutyCycle(0)
def driveLeft(): #Drive forwards and turn left
        pwmForwards.ChangeDutyCycle(40)
        pwmLeft.ChangeDutyCycle(15)
        sleep(1)
        pwmForwards.ChangeDutyCycle(0)
        pwmLeft.ChangeDutyCycle(0)
def STOP(): #Gracefully exit the program
        GPIO.cleanup()
        quit()

#Begin the program:

while(1):
        #Define shortcuts
        R = moveRight
        L = moveLeft
        F = moveForwards
        B = moveBackwards
        S = STOP
        #Run program
        run = input('What would you like to do? ')
        run()

#Demo controls (obsolete, for reference only)
#moveRight()
#moveForwards()
#sleep(1)
#moveBackwards()
#moveLeft()
#sleep(1)

#Clean up the GPIO pins to avoid errors on next run:
GPIO.cleanup()
