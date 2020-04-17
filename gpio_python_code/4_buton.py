#!/usr/bin/python



import os

from time import sleep

import RPi.GPIO as GPIO



GPIO.setmode(GPIO.BCM)




# setup our output pins

GPIO.setup(17,GPIO.OUT)

GPIO.setup(27,GPIO.OUT)




# setup our input pin

# we use an internal pull up resistor to hold the pin at 3v3, otherwise the inputs value could chatter between high and low



GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)



while True:

    if ( GPIO.input(10) == False ):

        print("Button Pressed")

        os.system('date') # print the systems date and time

        print GPIO.input(10)
        GPIO.output(17,GPIO.HIGH)
        GPIO.output(27,GPIO.HIGH) # set GPIO27 high, 3v3 will now be active on that pin

        sleep(2)
        GPIO.output(17,GPIO.LOW)
        sleep(2)
        GPIO.output(27,GPIO.LOW) # set GPIO27 high, 3v3 will now be active on that pin

    else:

        os.system('clear') # clear the screens text

        print ("Waiting for you to press a button")

        sleep(0.1)
