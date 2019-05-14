import pymysql.cursors
import time
# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             db='LJ',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print ("connect successful!!")

def curent_album_id(connection):
	# 'select id, max(id) from  list_album_id'
	with connection.cursor() as cursor:
		sql = 'SELECT *  FROM list_album_id WHERE id=(select  max(id) from  list_album_id)'
		cursor.execute(sql)
		result = cursor.fetchone()
		print(result)
	# return result['album_id']
curent_album_id(connection)
connection.close()
import time
from load_post_vk_class import vk_api, clean
src = 'https://1957anti.ru/media/k2/items/cache/ed665975b819d9e4bff8f3321152810d_XL.jpg'
album_id = 260959360
group_id = 165089751
token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
vk_user = vk_api.VkApi(token ,api_version='5.92')
vk_user.auth()
clean(group_id,vk_user)
# # with connection.cursor() as cursor:
# # 	sql = "create table list_group_id( group_id integer(11) not null)"
# # 	cursor.execute(sql)
# # connection.commit()
# # connection.close()
# # load_img_PIL(vk_user,group_id,src,album_id)
# with connection.cursor() as cursor:
# 	sql = "INSERT INTO list_album_id (album_id) VALUES (%s)"
# 	album_id =261028865
# 	cursor.execute(sql, (album_id,))
# connection.commit()
# connection.close()
# def getting_links_to_creare_db(connection,vk_user,group_id):
# 	list_saves=0
# 	try:
# 		with connection.cursor() as cursor:
# 			sql = "INSERT INTO URL_PUBLIC_POSTS (URL, DATE_PUBLIC) VALUES (%s, %s)"
# 			for i in range(0,400,100):
# 				zapros = vk_user.method('wall.get',{'owner_id':-group_id,'offset':i,'count':100})
# 				print(len(zapros))
# 				for zap in zapros[1:]:
# 					date = time.strftime('%Y-%m-%d',time.localtime(int(zap['date'])))
# 					link = zap['text'].split('<br>')[1]
# 					cursor.execute(sql, (link, date))
# 					list_saves += 1
# 		connection.commit()
# 	finally:
# 		connection.close()
# 	return list_saves

# def load_list_sav(connection, date=int(time.time())):
# 	try:
# 		with connection.cursor() as cursor:
# 			date = time.strftime('%Y-%m-%d',time.localtime(date))
# 			sql = "SELECT URL FROM URL_PUBLIC_POSTS WHERE DATE_PUBLIC > '{}' ".format(date)
# 			cursor.execute(sql)
# 			# help(cursor)
# 			result = cursor.fetchmany(103)
# 			# result = cursor.fetchone()
# 			# print(result)
# 	finally:
# 		connection.close()
# 		return [i['URL'] for i in result]
# # print(getting_links_to_creare_db(connection,vk_user,group_id))
# # load_list_sav(connection,  1549988746)


# # from datetime import datetime, date, timedelta
# # import time 
# # # help(time)
# # now_time = int(time.mktime(datetime.now().timetuple()))
# # next_day = int(time.mktime((date.today()+timedelta(days=1)).timetuple()))
# # for i in range(now_time+15, next_day ,(next_day-now_time)//2):
# # 	print(time.strftime('%H %M',time.localtime(i)))


import vk_api_my as vk_api
import pytube
import os
# help(os.remove)
# import pymedia
from io import BytesIO
# print(dir(pytube.YouTube))
# help(pytube.YouTube)
# data = bytearray()
from datetime import datetime, date, timedelta
import time
now_day =time.mktime(date.today().timetuple())
now_time = int(time.mktime(datetime.now().timetuple()))
next_day = int(time.mktime((date.today()+timedelta(days=1)).timetuple()))

print(now_time, next_day, now_day)
os._exit(1)

link = "https://www.youtube.com/watch?v=L1W0XvU_8M4"
yt = pytube.YouTube(link)

streams = yt.streams.first()
link_for_save = "/home/maksim/Загрузки/{}.{}".format(yt.title,streams.subtype)
# print(streams)
# print(dir(streams),streams.subtype,yt.title,sep='\n')
# # os.mkdir(data)
streams.download("/home/maksim/Загрузки/")
vk_user = vk_api.VkApi()
upload_url=vk_user.method('video.save',{'name':yt.title})['upload_url']
print(upload_url)

with open(link_for_save, 'rb') as video:	
	ur = vk_api.requests.post(upload_url,  files = {'video_file':video}).json() 
# print(ur)
os.remove(link_for_save)
link_video = "https://vk.com/video{}_{}".format(ur['owner_id'],ur['video_id'])

# # ur = vk_api.requests.post(upload_url, files = {'file1': foto}).json()
print(link_video)
