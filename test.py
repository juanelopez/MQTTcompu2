import threading
import queue
from concurrent import futures

q = queue.Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()
    return
def workerb():
    while True:
        for item in range(30):
            q.put(item)
            print(item)
        return
        #q2.task_done()
# Turn-on the worker thread.
#threading.Thread(target=worker, daemon=True).start()

#hilo.result()
# Send thirty task requests to the worker.
#for item in range(30):
#    q.put(item)
#    q2.put(item)
if __name__ == '__main__':
    # Block until all tasks are done.
    hilos = futures.ThreadPoolExecutor()
    a = hilos.submit(worker)
    b = hilos.submit(workerb)
    q.join()
    #q2.join()
    print('All work completed')
