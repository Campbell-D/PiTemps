import sched, time, threading
from datetime import datetime

scheduler = sched.scheduler(time.time, time.sleep)

def stuff(name):
	t = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
	print(t, "doing stuff", name)

def print_event(name): 
    print('EVENT:', time.time(), name) 




e1 = scheduler.enter(10, 1, stuff, ('1st', )) 
print ("e1:", e1)

e2 = scheduler.enter(15, 1, stuff, ('2nd', )) 
print ("e2:", e2)

# Start a thread to run the events
t = threading.Thread(target=scheduler.run)
t.start()

while not (scheduler.empty()):
# 	scheduler.run(blocking=False)
 	print(scheduler.queue)
 	time.sleep(3.3)


# Back in the main thread, cancel the first scheduled event.
#scheduler.cancel(e1)

# Wait for the scheduler to finish running in the thread
t.join()






