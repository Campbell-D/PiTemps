#!/usr/bin/python

import RPi.GPIO as GPIO # import a library
GPIO.setmode(GPIO.BCM) # set the pin numbering system to BCM
GPIO.setup(17,GPIO.OUT) # set GPIO17 as an OUTPUT
GPIO.setup(27,GPIO.OUT) # set GPIO27 as am OUTPUT

print "Lights on"

GPIO.output(17,GPIO.HIGH) # set GPIO17 high, 3v3 will now be active on that pin
GPIO.output(27,GPIO.HIGH) # set GPIO27 high, 3v3 will now be active on that pin


