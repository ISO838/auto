#Import libraries
import sys, tty, termios, time
from time import sleep
import RPi.GPIO as GPIO

#Set the GPIO pin configurations
GPIO.setmode(GPIO.BCM) #Use the BCM PIN numbering scheme
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT) #Drive Lights

#Define the output pins and PWM frequency
pwmForwards=GPIO.PWM(26,100)
pwmBackwards=GPIO.PWM(20,100)
pwmTurn=GPIO.PWM(17,50)

#Set up the global variables
steerState = "centre"
print "Steering is centered"
gearState = "neutral"
print"Gear is neutral"

# Define functions:
def sysStart(): #System startup process
        pwmForwards.start(0)
        pwmBackwards.start(0)
        pwmTurn.start(6.9)
        GPIO.output(27,1)
        sleep(0.2)
        GPIO.output(27,0)
        sleep(0.3)
        GPIO.output(27,1)
        pwmTurn.ChangeDutyCycle(0)
        print"The system is active and awaiting input"
def moveForwards(): #Move the main drive motor forwards
        pwmForwards.ChangeDutyCycle(55)
def moveForwards2(): #Move the main drive motor forwards quicker
        pwmForwards.ChangeDutyCycle(75)
def moveBackwards(): #Move the main drive motor backwards
        pwmBackwards.ChangeDutyCycle(35)
def allStop(): #Stop the main drive motor
        pwmForwards.ChangeDutyCycle(0)
        pwmBackwards.ChangeDutyCycle(0)
def wheelStraight(): #Centre the steering
        pwmTurn.ChangeDutyCycle(7)
        sleep(0.3)
        pwmTurn.ChangeDutyCycle(0)
def moveRight(): #Turn the wheel to the right
        pwmTurn.ChangeDutyCycle(2)
        sleep(0.3)
        pwmTurn.ChangeDutyCycle(0)
def moveLeft(): #Turn the wheel to the left
        pwmTurn.ChangeDutyCycle(11)
        sleep(0.3)
        pwmTurn.ChangeDutyCycle(0)
def STOP(): #Gracefully exit the program
        print"The system is shuting down"
        char = ""
        GPIO.cleanup()
        quit()
def getch(): #Reads user iput over SSH session
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd,termios.TCSADRAIN, old_settings)
        return ch

def gearing(gear):
        global gearState
        if(gear == "gear1"):
                if(gearState == "neutral"):
                        moveForwards()
                        gearState = "gear1"
                        print"gear 1"
                elif(gearState == "gear-1"):
                        allStop()
                        gearState = "neutral"
                        print"neutral"
        if(gear == "gear-1"):
                if(gearState == "neutral"):
                        moveBackwards()
                        gearState = "gear-1"
                        print"gear -1"
                elif(gearState == "gear1"):
                        allStop()
                        gearState = "neutral"
                        print"neutral"
#       if(gear == "gear2"):
#               if(gearState == "gear-1"):
#                       moveForwards()
#                       print"gear 1"
#       if(gear == "gear-1"):
#               if(gearState == "gear1"):
#                       allStop()
#                       gearState = "neutral"
#                       print"neutral"


def steering(direction):
        global steerState
        if(direction == "right"):
                if(steerState == "centre"):
                        moveRight()
                        steerState = "right"
                        print"right"
                elif(steerState == "left"):
                        wheelStraight()
                        steerState = "centre"
                        print"centre"
        if(direction == "left"):
                if(steerState == "centre"):
                        moveLeft()
                        steerState = "left"
                        print"left"
                elif(steerState == "right"):
                        wheelStraight()
                        steerState = "centre"
                        print"centre"

sysStart()
while(1):
        #Define shortcuts
        char = getch()
        if(char == "I"):
                gearing("gear1")
        if(char == "K"):
                gearing("gear-1")
        if(char == "J"):
                steering("left")
        if(char == "L"):
                steering("right")
        if(char == "X"):
                allStop()
                STOP()

#Run program
        #run = input('What would you like to do? ')
        #run()


#Clean up the GPIO pins to avoid errors on next run:
GPIO.cleanup()
