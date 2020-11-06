import time
from time import gmtime, strftime
import threading
import queue



## for integration with other functions need to change all the prints to the queue, and add locks when requiring user-inputs.


            
def timestamp(lock, messages):

## function of stopwatch: display the time every second and messages, if exist in queue. Argument "messages" is a queue, to which all messages from other functions are passed

    while True:
        while (not lock.locked() and messages.empty()):
            print(strftime("%H:%M:%S", gmtime()))
            time.sleep(1)

        else:
            message = messages.get()
            print(message)

            
if __name__ == "__main__":

    messages = queue.Queue()
    lock = threading.Lock()

    
    x = threading.Thread(target=timestamp, args = (lock, messages,))
    x.daemon = True
    x.start()
  
# add other functions to y thread to be executed simultaneously with stopwatch
#    y = threading.Thread(target = <function>, args = (<arg>,))
#    y.start()

