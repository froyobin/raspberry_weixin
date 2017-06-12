#!/usr/bin/python2.7
import RPi.GPIO as GPIO
import time
import threading
import datetime

led_pin = 26
sensor_pin = 19
light_state = False
should_close = False
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin,GPIO.OUT)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin,GPIO.IN)

def hello():
    global  light_state
    if should_close == False:
        return
    light_state = False
    should_cose = False
    GPIO.output(led_pin, True)


#def light_handler(args,args2):
#    global light_state
#    while() :
#        print "in handler"
#        if light_state == False:
#            GPIO.output(led_pin, True)
#        else:
#            GPIO.output(led_pin, False)
#        time.sleep(0.2)

def main():
    global light_state
    global should_close
    off_counter = 0
    #threading.start_new_thread(light_handler,('MyStringHere',1))
    while True:
        hours = datetime.datetime.now().timetuple().tm_hour
	if hours >7 and hours< 23:
            #print "skip...."
            time.sleep(20)
	    continue
        if (GPIO.input(sensor_pin)):
            #print "triggled"
            if light_state == False:
	        light_state = True
		should_close = True
	        GPIO.output(led_pin, False)
                timer = threading.Timer(180, hello)
                timer.start()
		time.sleep(3)
		continue
            #if light_state == True:
                #if (GPIO.input(sensor_pin)):
	    #    light_state = False
	    #    GPIO.output(led_pin, True)
#		time.sleep(3)
 #               continue
                
        #else:
	#    print "turn off"
            #off_counter += 1
            #if off_counter >5:
            #    light_state = False
            #    off_counter = 0


        time.sleep(1)
if __name__ == "__main__":
    main()
