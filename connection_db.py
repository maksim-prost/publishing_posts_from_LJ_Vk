import pymysql.cursors
import time
# Connect to the database
from datetime import datetime, date, timedelta
# now_time = int(time.mktime(datetime.now().timetuple()))
# prev_day = int(time.mktime((date.today()-timedelta(days=1)).timetuple()))
		

class InteractionWithDB():
	def __init__(self):
		self.connection = pymysql.connect(host='localhost',
                             user='bootLJ',
                             password='1234',
                             db='LJ',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	def __del__(self):
		self.connection.close()
	def load_list_save(self,date=1518452746):
		try:
			result = []
			with self.connection.cursor() as cursor:
				date = time.strftime('%Y-%m-%d',time.localtime(date))
				sql = "SELECT URL FROM URL_PUBLIC_POSTS WHERE DATE_PUBLIC > '{}' ".format(date)
				cursor.execute(sql)
				result = cursor.fetchall()
		finally:
			return [i['URL'] for i in result]
	def uppdate_link(self,list_to_save):
		with self.connection.cursor() as cursor:
			sql = "INSERT INTO URL_PUBLIC_POSTS (URL, DATE_PUBLIC) VALUES (%s, %s)"
			for url in list_to_save:
				cursor.execute(sql, (url, time.strftime('%Y-%m-%d')))
				# print('commit url', url)
		self.connection.commit()
	def count_today_posts(self):
		try:
			with self.connection.cursor() as cursor:
				prev_day = int(time.mktime((date.today()-timedelta(days=1)).timetuple()))
				cdate = time.strftime('%Y-%m-%d',time.localtime(prev_day))
				sql = "SELECT COUNT(*) FROM URL_PUBLIC_POSTS WHERE DATE_PUBLIC > '{}'".format(cdate)
				cursor.execute(sql)
				result = cursor.fetchone()
				# print(result)
		finally:
			return result['COUNT(*)']
	def uppdate_album_id(self,album_id):
		with self.connection.cursor() as cursor:
			sql = "INSERT INTO list_album_id (album_id) VALUES (%s)"
			cursor.execute(sql, (album_id,))
		self.connection.commit()
	def list_album_id(self):
		with self.connection.cursor() as cursor:
			sql = 'SELECT album_id  FROM list_album_id'
			cursor.execute(sql)
			result =[i['album_id'] for i in cursor.fetchall()]
		return result

	def curent_album_id(self):
		# 'select album_id, max(id) from  list_album_id'
		with self.connection.cursor() as cursor:
			sql = 'SELECT *  FROM list_album_id WHERE id=(select  max(id) from  list_album_id)'
			cursor.execute(sql)
			result = cursor.fetchone()
		return result['album_id']

if __name__ == '__main__':
	test = InteractionWithDB()
