import json
import glob, os
from datetime import datetime
import RPi.GPIO as GPIO # import our GPIO library
import sched, time, threading

scheduler = sched.scheduler(time.time, time.sleep)
reading_active=False
button_pressed=0

GPIO.setmode(GPIO.BCM) # set the board numbering system to BCM
GPIO.setup(17,GPIO.OUT) # LED
GPIO.setup(22,GPIO.OUT) # Buzzer 
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button

def write_out(outputs):
    # print(outputs)
    outfile = open(output_file, "w")
    for t in outputs:
        outfile.write("[" + str(t) + "]")
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    outfile.write("\nLast update: " + str(t))
    outfile.close()

def write_csv(outputs):
    # print(outputs)
    outfile = open(csv_file, "a")
    tim = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    outstr=tim
    for t in outputs:
        outstr = outstr + ","+str(t)
    outstr = outstr + "\n"
    outfile.write(outstr)
    outfile.close()


def button_callback(channel):
    print("Ok, who pressed the button?")
    global button_pressed
    button_pressed += 1
    time.sleep(0.5)
    if (button_pressed > 3):
        global loops
        global count
        loops = count+1
        print("so many button presses",button_pressed)
        return
    else:
        print("Keep a clicking", button_pressed)

def read_temp_raw(device_file):
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def blink ():
    if not reading_active:
        GPIO.output(17,GPIO.HIGH)
        time.sleep(.06)
        GPIO.output(17,GPIO.LOW)

def read_temp():
    global reading_active
    reading_active=True
    e1 = scheduler.enter(interval, 1, read_temp, ()) 
    GPIO.output(17,GPIO.HIGH)
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    global loops
    loops += 1
    temp_c = 0
    item_index = 0
    outputs=[999,999,999,999,999]
    for item in config_data['devices']:
            id = item["id"]
            device_file = base_dir + '/' + id + '/w1_slave'
            # print(item_index, device_file)
            try:
                lines = read_temp_raw(device_file)
                while lines[0].strip()[-3:] != 'YES':
                    time.sleep(0.2)
                    lines = read_temp_raw()
                equals_pos = lines[1].find('t=')
            except:
                equals_pos = -1
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = float(temp_string) / 1000.0
                outputs[item_index]=temp_c
            else:
                outputs[item_index]=998
            item_index += 1
    print(t, outputs)
    reading_active=False

    write_out(outputs)
    write_csv(outputs)


    # for device_folder in device_folders:
    #     device_id = os.path.basename(device_folder)
    #     device_file = device_folder + '/w1_slave'
    #     # print(device_file, device_id)

    #     try:
    #         lines = read_temp_raw(device_file)
    #         while lines[0].strip()[-3:] != 'YES':
    #             time.sleep(0.2)
    #             lines = read_temp_raw()
    #         equals_pos = lines[1].find('t=')
    #     except:
    #         equals_pos = -1
    #     global loops
    #     global count
    #     loops += 1
    #     # print("Reading", loops, "of", count)

    #     if equals_pos != -1:
    #         temp_string = lines[1][equals_pos+2:]
    #         temp_c = float(temp_string) / 1000.0
    #         #temp_f = temp_c * 9.0 / 5.0 + 32.0
    #         GPIO.output(17,GPIO.LOW)
    #         # read through the list of dictionaries read from config then pull out the name or set a catch-all
    #         device_dict = next((item for item in config_data['devices'] if item["id"] == device_id), {'id': device_id, 'name': 'Unknown_Sensor'})
    #         # print(device_dict)
    #         device_name=device_dict['name']
    #         print(t, device_id, device_name, temp_c)
    GPIO.output(17,GPIO.LOW)
    return #temp_c 

def read_config():
	with open('logger.json', 'r') as config_file:
	    data=config_file.read()
	cd = json.loads(data)
	return cd


GPIO.add_event_detect(10, GPIO.RISING, callback=button_callback)


base_dir = '/sys/bus/w1/devices/'
# device_folder = glob.glob(base_dir + '28*')[0]
# device_file = device_folder + '/w1_slave'
# device_folders = glob.glob(base_dir + '28*')



	# parse file
config_data = read_config()

# show config data
# print("config_data:\t" + str(config_data))

print("\noutput_file:\t" + str(config_data['output_file']))
print("interval:   \t" + str(config_data['interval']))
print("count:      \t" + str(config_data['count']))
devices = config_data['devices']
print("devices:    \t", devices)
# device_name=()
# for l in config_data['devices']:
#     print(l)
#     device_name{l['id']}=l['name']
# print(device_name)
print("\n")

interval = config_data['interval']
count = config_data['count']
output_file = config_data['output_file']
try:
    os.remove(output_file)
except:
    pass

csv_file = config_data['csv_file']

# loop_count = config_data['count']
# while loop_count > 0:
#     loop_count = loop_count - 1
#     print(loop_count)
#     tempy=read_temp()
#     t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     print(t, tempy)
#     time.sleep(config_data['interval'])

loops=0
e1 = scheduler.enter(1, 1, read_temp, ()) 
# Start a thread to run the events
t = threading.Thread(target=scheduler.run, daemon=True)
t.start()

while not (scheduler.empty()):
    # if(GPIO.input(10) == False) or (loops >= count):
    button_pressed -=1
    if (button_pressed <0 ):
        button_pressed = 0
    # print("buttons", button_pressed)
    if(loops >= count) or (os.path.exists('logger.abort')):
        print("Canceling on button press or completed")
        time.sleep(2)
        print("Clearing logging queue...")
        for  q in scheduler.queue:
            print("...")
            scheduler.cancel(q)
    time.sleep(6)
    blink()
# print("Jobs left:",scheduler.queue)
# time.sleep(interval)
print ("Deleting output file...")
try:
    os.remove(output_file)
except:
    pass
try:
    os.remove('logger.abort')
except:
    pass

# t.join()
print ("Tidying up GPIO...")
GPIO.output(17,GPIO.LOW)
GPIO.cleanup()



