#Libraries
import RPi.GPIO as GPIO
import time
import os
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

#sudo pigpiod

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
RED_LED=25
 
#set Servo motor
factory = PiGPIOFactory()
servo = Servo(26, pin_factory=factory)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(RED_LED,GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def turnOnRedLed():
    GPIO.output(RED_LED,True)
    
def turnOffRedLed():
    GPIO.output(RED_LED,False)
    
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            if(dist<30):
                turnOnRedLed()
                if(servo.value!=1):
                    servo.max()
                
            else:
                turnOffRedLed()
                if(servo.value!=-1):
                    servo.min()
                
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo.value=None
        GPIO.cleanup()
