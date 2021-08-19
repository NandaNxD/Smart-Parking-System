#Libraries
import RPi.GPIO as GPIO
import time
 
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


if __name__ == '__main__':
    #set GPIO Pins
    GPIO_TRIGGER1 = 22
    GPIO_ECHO1 = 4
    GPIO_TRIGGER2 = 20
    GPIO_ECHO2 = 23
    RED_LED=12

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
    GPIO.setup(GPIO_ECHO1, GPIO.IN)
    GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
    GPIO.setup(GPIO_ECHO2, GPIO.IN)
    GPIO.setup(RED_LED,GPIO.OUT)
    
    try:
        while True:
            dist1=100
            dist2=200
            
            dist1 = distance(GPIO_TRIGGER1,GPIO_ECHO1)
            time.sleep(0.1)
            dist2= distance(GPIO_TRIGGER2,GPIO_ECHO2)
            
            if(dist1<30 and dist2<30):
                GPIO.output(RED_LED,True)
            else:
                GPIO.output(RED_LED,False)
                
            print ("Measured Distance = %.2f cm" % dist1)
            print("Measured Distance= %.2f cm" %dist2)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
