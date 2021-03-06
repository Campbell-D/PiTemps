import json
import glob, os
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO # import our GPIO library
GPIO.setmode(GPIO.BCM) # set the board numbering system to BCM
GPIO.setup(17,GPIO.OUT) # LED
GPIO.setup(22,GPIO.OUT) # Buzzer 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    GPIO.output(17,GPIO.HIGH)
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        GPIO.output(17,GPIO.LOW)
        return temp_c 

def read_config():
	with open('logger.json', 'r') as config_file:
	    data=config_file.read()
	cd = json.loads(data)
	return cd

	# parse file
config_data = read_config()

# show config data
print("config_data:\t" + str(config_data))
print("output_file:\t" + str(config_data['output_file']))
print("interval:   \t" + str(config_data['interval']))
print("count:      \t" + str(config_data['count']))

loop_count = config_data['count']
while loop_count > 0:
    loop_count = loop_count - 1
    print(loop_count)
    tempy=read_temp()
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(t, tempy)
    sleep(config_data['interval'])




GPIO.output(17,GPIO.LOW)
GPIO.cleanup()



