from time import sleep
from rq import Queue
from worker import conn
from get_data_from_LJ_class import main
def message(msg):
	print(msg)

# q = Queue(connection=conn)
token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
group_id =165089751 #чат-бот
user_id= 117562096

while 1:
	# print()
	# q.enqueue(message,'Hello meeting through 300')
	main(token, group_id, user_id)
	sleep(3000)
