from time import sleep
from rq import Queue
from worker import conn

def message(msg):
	print(msg)

q = Queue(connection=conn)


while 1:
	# print()
	q.enqueue(message,'Hello meeting through 300')
	sleep(300)
