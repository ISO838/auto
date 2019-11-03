#Import libraries
import sys, tty, termios, time
from time import sleep
import RPi.GPIO as GPIO

#Set the GPIO pin configurations
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

#Define the output pins and PWM frequency
pwmForwards=GPIO.PWM(26,100)
pwmBackwards=GPIO.PWM(20,100)
pwmTurn=GPIO.PWM(17,50)

#Set up the system
#Start the PWM process and set the Duty Cycle
pwmForwards.start(0)
pwmBackwards.start(0)
pwmTurn.start(6.9) #Centre the wheels on system start
sleep(0.5)
pwmTurn.ChangeDutyCycle(0)
steerState = "centre"
print"The system is active and awaiting input"

# Motor functions:
def moveForwards(): #Move the main drive motor forwards
        pwmForwards.ChangeDutyCycle(55)
        print"Moving forwards"
def moveBackwards(): #Move the main drive motor backwards
        pwmBackwards.ChangeDutyCycle(35)
        print"Moving backwards"
def allStop(): #Stop the drive motor
        pwmForwards.ChangeDutyCycle(0)
        pwmBackwards.ChangeDutyCycle(0)
        print"All stop"
def wheelStraight(): #Straighten the steering
        pwmTurn.ChangeDutyCycle(7)
        sleep(0.3)
        pwmTurn.ChangeDutyCycle(0)
        print"Wheels straight"
def moveRight(): #Turn the wheel to the right
        print"Move right"
        pwmTurn.ChangeDutyCycle(2)
        sleep(0.3)
        pwmTurn.ChangeDutyCycle(0)
def moveLeft(): #Turn the wheel to the left
        print"Move left"
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
def steering(direction):
        global steerState
        if(direction == "right"):
                if(steerState == "centre"):
                        moveRight
                        steerState = "right"
                        print"steerState"
                elif(steerState == "left"):
                        wheelStraight
                        steerState = "centre"
                        print"steerState"
        if(direction == "left"):
                if(steerState == "centre"):
                        moveLeft
                        steerState = "left"
                        print"steerState"
                elif(steerState == "right"):
                        wheelStraight
                        steerState = "centre"
                        print"steerState"

while(1):
        #Define shortcuts
        R = moveRight
        L = moveLeft
        F = moveForwards
        B = moveBackwards
        S = wheelStraight
        Q = allStop
        char = getch()
        if(char == "I"):
                F
        if(char == "K"):
                Q
        if(char == "J"):
                steering("left")
        if(char == "L"):
                steering("right")
        if(char == "X"):
                STOP
        Q

#Run program
        #run = input('What would you like to do? ')
        #run()


#Clean up the GPIO pins to avoid errors on next run:
GPIO.cleanup()

