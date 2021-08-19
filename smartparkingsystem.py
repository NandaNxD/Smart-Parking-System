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


def distance(GPIO_TRIGGER,GPIO_ECHO):
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


def turnOnRedLed(LED_PIN):
    GPIO.output(LED_PIN,True)
    
def turnOffRedLed(LED_PIN):
    GPIO.output(LED_PIN,False)

def buzzerOn(BUZZER_PIN):
    GPIO.output(BUZZER_PIN,True)
    
def buzzerOff(BUZZER_PIN):
    GPIO.output(BUZZER_PIN,False)
    
    
if __name__ == '__main__':
    GPIO_TRIGGER1 = 22
    GPIO_ECHO1 = 4
    GPIO_TRIGGER2 = 20
    GPIO_ECHO2 = 23
    LED_PIN=12
    BUZZER_PIN=16

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
    GPIO.setup(GPIO_ECHO1, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
    GPIO.setup(GPIO_ECHO2, GPIO.IN)
    GPIO.setup(LED_PIN,GPIO.OUT)
    GPIO.setup(BUZZER_PIN,GPIO.OUT)

    factory = PiGPIOFactory()
    servo = Servo(26, pin_factory=factory)
    GPIO.setwarnings(False)

    try:
        while True:
            dist1 = distance(GPIO_TRIGGER1,GPIO_ECHO1)
            time.sleep(0.1)
            dist2 = distance(GPIO_TRIGGER2,GPIO_ECHO2)

            if(dist1<30 or dist2<30):
                turnOnRedLed(LED_PIN)
                if(servo.value!=1):
                    servo.max()
                
                buzzerOn(BUZZER_PIN)
                time.sleep(0.5)
                buzzerOff(BUZZER_PIN)
                
            else:
                turnOffRedLed(LED_PIN)
                if(servo.value!=-1):
                    servo.min()
                
            print ("Measured Distance = %.1f cm" % dist1)
            print ("Measured Distance = %.1f cm" % dist2)
            time.sleep(0.5)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo.value=None
        GPIO.cleanup()
