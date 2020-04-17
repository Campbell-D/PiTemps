import time
import RPi.GPIO as GPIO

print(GPIO.getmode())
GPIO.setmode(GPIO.BCM)
print(GPIO.getmode())
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def my_callback(channel):
    print("Buttons for everyone!")

GPIO.add_event_detect(10, GPIO.RISING, callback=my_callback)

# you can continue doing other stuff here
while True:
    print(GPIO.input(10))
    time.sleep(1)
