class A:
    x = 1

    @staticmethod  # Define as class method because it affects class state
    def t(a):
        A.x = a

class B(A):
    ...

class C(A):
    ...

print(A.x)
print(B.x)
print(C.x)
C.x = 2
A.x = 3
print(A.x)
print(B.x)
print(C.x)

"""# Adapted from various articles from SuperFastPython.com
# example of thread-safe writing to a file with a dedicated writer thread
from random import random
from queue import Queue
from threading import Event
import concurrent.futures as futures


# dedicated file writing task
def fileWriter(filepath, queue: Queue, event: Event):
    # open the file
    with open(filepath, 'w') as file:
        # run forever
        while not event.is_set() or queue.qsize() > 0:
            # get a line of text from the queue
            line = queue.get()
            # write it to file
            file.write(line)
            # flush the buffer
            file.flush()
            # mark the unit of work complete
            queue.task_done()


# task for worker threads
def task(number, queue):
    # task loop
    for i in range(1000):
        # generate random number between 0 and 1
        value = random()
        # put the result in the queue
        queue.put(f'Thread {number} got {value}.\n')


event = Event()
queue = Queue()

filepath = 'output.txt'

# open the file
with open(filepath, 'a') as file:
    with futures.ThreadPoolExecutor(1001) as exe:
        writer_future = exe.submit(fileWriter, filepath, queue, event)

        thread_futures = [exe.submit(task, i, queue) for i in range(1000)]
        futures.wait(thread_futures, return_when=futures.ALL_COMPLETED)
        event.set()
"""