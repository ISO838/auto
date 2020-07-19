#Import libraries
import sys, tty, termios, time
from time import sleep
import RPi.GPIO as GPIO

#Set the GPIO pin configurations
GPIO.setmode(GPIO.BCM) #Use the BCM PIN numbering scheme
GPIO.setup(26, GPIO.OUT) #Drive motor forwards
GPIO.setup(20, GPIO.OUT) #Drive motor backwards
GPIO.setup(17, GPIO.OUT) #Steering servo
GPIO.setup(27, GPIO.OUT) #Drive Lights
GPIO.setup(24, GPIO.OUT) #Tail Lights
GPIO.setup(23, GPIO.OUT) #Left-hand indicators
GPIO.setup(22, GPIO.OUT) #Right-hand indicators

#Define the output pins and PWM frequency
pwmForwards=GPIO.PWM(26,100)
pwmBackwards=GPIO.PWM(20,100)
pwmTurn=GPIO.PWM(17,50)
pwmTail=GPIO.PWM(24,70)
pwmLIndi=GPIO.PWM(23,2)
pwmRIndi=GPIO.PWM(22,2)

#Set up the global variables
steerState = "centre"
print("Steering is centered")
gearState = "neutral"
print("Gear is neutral")

# Define functions:
def sysStart(): #System startup process
        pwmForwards.start(0)
        pwmBackwards.start(0)
        pwmTurn.start(6.9)
        pwmTail.start(100)
        pwmTail.ChangeDutyCycle(50) #Turn on tail lights
        GPIO.output(27,1) #Drive lights on
        sleep(0.2)
        GPIO.output(27,0) #Drive lights off
        sleep(0.3)
        GPIO.output(27,1) #Drive light on
        pwmTurn.ChangeDutyCycle(0)
        print("The system is active and awaiting input")
def moveForwards(): #Move the main drive motor forwards
        pwmTail.ChangeDutyCycle(10) #Turn off brakelights
        pwmForwards.ChangeDutyCycle(90)
def moveBackwards(): #Move the main drive motor backwards
        pwmTail.ChangeDutyCycle(10) #Turn off brakelights
        pwmBackwards.ChangeDutyCycle(75)
def allStop(): #Stop the main drive motor
        pwmForwards.ChangeDutyCycle(0)
        pwmBackwards.ChangeDutyCycle(0)
        pwmTail.ChangeDutyCycle(100) #Turn on brakelights
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
def indicateLeft(): #Indicate left
        print("Left indicator on")
        pwmLIndi.start(50)
def indicateRight(): #Indicate right
        print("Right indicator on")
        pwmRIndi.start(50)
def hazard(): #Hazard lights
        print("Hazard lights on")
        pwmRIndi.start(50)
        pwmLIndi.start(50)
def indicateStop(): #Stop indicating
        pwmRIndi.start(0)
        pwmLIndi.start(0)
def STOP(): #Gracefully exit the program
        print("The system is shuting down")
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
def gearing(gear): #Controls the gear selection
        global gearState
        if(gear == "gear+1"):
                if(gearState == "neutral"):
                        gearState = "gear1"
                        print("gear 1")
                elif(gearState == "gear-1"):
                        gearState = "neutral"
                        print("neutral")
        if(gear == "gear-1"):
                if(gearState == "neutral"):
                        gearState = "gear-1"
                        print("gear -1")
                elif(gearState == "gear1"):
                        gearState = "neutral"
                        print("neutral")
#       if(gear == "gear2"):
#               if(gearState == "gear-1"):
#                       moveForwards()
#                       print"gear 1"
#       if(gear == "gear-1"):
#               if(gearState == "gear1"):
#                       allStop()
#                       gearState = "neutral"
#                       print"neutral"
def steering(direction): #Controls the direction selection
        global steerState
        if(direction == "right"):
                if(steerState == "centre"):
                        moveRight()
                        steerState = "right"
                        print("right")
                elif(steerState == "left"):
                        wheelStraight()
                        steerState = "centre"
                        print("centre")
        if(direction == "left"):
                if(steerState == "centre"):
                        moveLeft()
                        steerState = "left"
                        print("left")
                elif(steerState == "right"):
                        wheelStraight()
                        steerState = "centre"
                        print("centre")

sysStart()
while(1):
        #Define shortcuts
        char = getch()
        if(char == "2"):
                gearing("gear+1")
        if(char == "1"):
                gearing("gear-1")
        if(char == "I" and gearState == "neutral"):
                allStop()
                print("Not in gear!")
        if(char == "I" and gearState == "gear1"):
                moveForwards()
        if(char == "K"):
                allStop()
        if(char == "J"):
                steering("left")
        if(char == "L"):
                steering("right")
        if(char == "U"):
                indicateLeft()
        if(char == "O"):
                indicateRight()
        if(char == "H"):
                hazard()
        if(char == "G"):
                indicateStop()
        if(char == "X"):
                allStop()
                STOP()

#Run program
        #run = input('What would you like to do? ')
        #run()


#Clean up the GPIO pins to avoid errors on next run:
GPIO.cleanup()












