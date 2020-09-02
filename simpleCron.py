from datetime import datetime
import sched, time
# s =  sched.scheduler(time.time,time.sleep)
# def run(s):
#     print(datetime.now())
#     s.enter(30,1,run,(s,))

# s.enter(30,1,run,(s,))
# s.run
timeS = time.time()
while True:
    print(datetime.now())
    time.sleep(30)