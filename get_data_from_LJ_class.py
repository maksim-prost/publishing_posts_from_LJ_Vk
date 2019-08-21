#! ../venv/bin/python
#! /usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os, sys

import traceback
from datetime import datetime, date, timedelta
import time
from format_html import format_post
from load_post_vk_class import Load_Post #, load_post as load_post_vk
from load_image import get_html




class Wrapper:
	def __init__(self, object, chek=True):
		self.wrapper = object
		self.chek = chek
		
	def __getattr__(self,attrname):
		if self.chek: print(self.wrapper.__class__.__name__,  attrname)
		return getattr(self.wrapper, attrname)

class Debug:
	def __init__(self, chek):
		self.chek = chek
	def __getattribute__(self, attr): # Вызывается операцией [obj.any]
		if object.__getattribute__(self, 'chek'): 
			print(object.__getattribute__(self, '__class__'),attr)
		return object.__getattribute__(self, attr)
class PostBlog(Debug):
	lp = None
	token,group_id, user_id = None, None, None
	def __init__(self,url,creator,token,group_id, user_id,chek=True):
		Debug.__init__(self,chek=True)
		PostBlog.group_id = PostBlog.group_id or group_id
		PostBlog.user_id =  PostBlog.user_id or user_id
		PostBlog.lp = PostBlog.lp or Wrapper(Load_Post(group_id, user_id,token),True)
		self.url = url
		self.creator = creator
		self.list_link_post =self.get_list_data_for_public_bloger()
	@classmethod
	def count_public_post(cls):
		return cls.lp.return_count_puplic_post()
# 	def public_post (self):
# 		for url in self.list_link_post:
# 			try:
# 				name_post = 'Eror load post'
# 				name_post = "{}  от {}".format(self.function_load(url),datetime.now().strftime('%d-%m-%Y')
# )
# 				# i = self.count_public_post()
# 				# print('time_public ', url, time_public(i))
# 				PostBlog.lp.load_post(name_post,self.post_for_public,url)#,time_public(i))
# 			except:
# 				print(traceback.format_exc())
# 				print(name_post , url, 'ошибка при сохранение, необходим обработчик данной ошибки')
# 		return self.count_public_post()
	@classmethod
	def clean_album(cls):
		cls.lp.clean()
	def function_load(self,url,title):
		raise Exception('Метод д/б определен в дочернем классе')
	def get_list_data_for_public(self,list_date,list_header,begining=1,end=None,list_urls=None):
		soup = BeautifulSoup(get_html(self.url), 'lxml')
		# print(list_urls)
		list_urls = list_urls or list_header
		return [(url.get('href'),head.text,date.text) 
			for (url,head,date) in 
				zip(soup.find_all(*list_urls)[begining:end],
					soup.find_all(*list_header)[begining:end],
					soup.find_all(*list_date)[begining:end]) ]
		

		# dates = [date.text for date in soup.find_all(*list_date)[begining:end]]
		# headers = [head.text for head in soup.find_all(*list_header)[begining:end]]
		# urls = [url.get('href') for url in soup.find_all(*list_urls)[begining:end]]
		# return zip(urls,headers,dates)
		
	def public_current_post(self, list_data):
		# print(list_data)
		for url,head,date in list_data:
			# name_post.replace('\n', ' ')
			# title = title.replace('"','')
			name_post = "{}  от {}".format(' '.join(head.replace('"','').split()),date)
			# print(name_post, not name_post in PostBlog.lp.list_saves,sep='\n')
			if  not name_post in PostBlog.lp.list_saves:
				# print()
				self.function_load(url,head)
				PostBlog.lp.load_post(name_post,self.post_for_public,url)
	def load_post(self,url,title,soup,prefix=''):
		if title:
			self.post_for_public = format_post(soup,prefix) + '\n[{}| {}]'.format(url,self.creator)			

class Bulgat(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://bulgat.livejournal.com/','bulgat',*args)
	def  get_list_data_for_public_bloger(self,begining=0):
		list_date = ('abbr' ,{'class':"updated"})
		list_header = ('dt', {'class':"entry-title"})
		list_urls = ('a', {'class':"subj-link"})
		self.public_current_post(PostBlog.get_list_data_for_public(self,list_date,list_header,begining,2,list_urls))
	def function_load(self,url,title):
		# print(url)
		soup = BeautifulSoup(get_html(url), 'lxml')
		post = soup.find('div',class_='entry-content')
		self.load_post(url,title,post)

class BlauKraeh(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://blau-kraehe.livejournal.com/','Яна Завацкая',*args)
	def  get_list_data_for_public_bloger(self,begining=1):
		list_date = ('abbr', {'class':"datetime"})
		list_header = ('a', {'class':"subj-link"})
		self.public_current_post(PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3))
		
	def function_load(self,url,title):
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		post = soup.find('article', class_="b-singlepost-body entry-content e-content")
		self.load_post(url,title,post)
		return title
class Botya(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://botya.livejournal.com/','botya',*args)
	def  get_list_data_for_public_bloger(self,begining=0):
		list_date =('span',{'class':"entryHeaderDate"} )
		list_header= ('a', {'class':"subj-link"})
		self.public_current_post(
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3))
	def function_load(self,url,title): 
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		post = soup.find('article', class_="b-singlepost-body entry-content e-content")
		self.load_post(url,title,post)
		return title
class ONB(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://onb2017.livejournal.com/','ONB 2017',*args)
	def  get_list_data_for_public_bloger(self,begining=2):
		list_header = ('h3', {'class':"entryunit__title"})
		list_date = ('span' ,{'class':"date-entryunit__day"})
		list_urls =  ('link',{'itemprop':"url"})
		self.public_current_post(
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,4,list_urls))
	
	def function_load(self,url,title): 
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		post = soup.find("div", class_="b-singlepost-bodywrapper")
		self.load_post(url,title,post)
		return title	
class Ballaev(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://p-balaev.livejournal.com/','Петр Балаев',*args)
	def  get_list_data_for_public_bloger(self,begining=1):
		list_date = ('abbr' ,{'class':"updated"})
		list_header = ('a',{'class':"subj-link"})

		self.public_current_post(
			[(url,header,date) for (url,header,date) in 
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,8) 
			if ('https://p-balaev.livejournal'in url and 'Мои твиты' not in header)])
	
	def function_load(self,url,title):
		soup = get_html(url)
		post = BeautifulSoup(soup, 'lxml').find('div',class_='entry-content')
		self.load_post(url,title,post)
		return title
class Remi(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://remi-meisner.livejournal.com/?skip=2',
			'Реми Майнсер',*args)
	def  get_list_data_for_public_bloger(self,begining=None):
		list_date =('abbr', {'class':"updated"} )
		list_header= ('a', {'class':"subj-link"})
		self.public_current_post(
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3))
	def function_load(self,url,title): 
		post =  BeautifulSoup(get_html(url), 'lxml').find('div',class_='entry-content')
		self.load_post(url,title,post)
		return title
class Class1957(PostBlog):
	def __init__(self,*args):
		self.sufics = ('/classics','/publications')
		PostBlog.__init__(self,'https://1957anti.ru',
			'ОД имени Антипартийной группы 1957',*args)
	def  get_list_data_for_public_bloger(self,begining=None):
		find_all = ('article',{'class':"publications-category-item groupLeading"})
		find = ('a',)
		url = self.url
		for sufics in self.sufics:
			self.url = url+sufics
			PostBlog.get_list_data_for_public(self,list_date,list_header,None,begining,3)
		self.url = url
		self.list_link_post = [url+link for link in self.list_link_post if url+link not in PostBlog.lp.list_saves ]
		# print(len(self.list_link_post), self.list_link_post)
		return len(self.list_link_post)
	def function_load(self,url,title): 
		post=BeautifulSoup(get_html(url), 'lxml').find('div', class_="main-block")
		title = post.find('h1').text
		if 'publications' in url:
			tag = 'article'
			self.creator = post.find('a').text
		else:
			tag  = 'div'
			creator = post.find('div', class_="article-item-text").find('em') or \
			post.find('div', class_="classics-item-extra-block").find('li')

			self.creator = creator.text.strip().replace('„','').replace('“','').replace('"','').replace('/','')
		# print(creator)
		self.load_post(url,title,post.find(tag, class_="article-item-body"), self.url)
		return title

class Conteiner_Blogs:
	def __init__(self,*arg):
		# list_blog = Botya,Remi,BlauKraeh,Class1957,Bulgat, Ballaev,ONB, 
		list_blog =  Bulgat, Botya, BlauKraeh, Ballaev, ONB, Remi,
		self.blogers=[blog(*arg) for blog in list_blog]
	

def main(token, group_id, user_id, creator='ALL',url_creator=None):
	
	# message_display = MessageDisplay()
	# print("Запуск парсинга, в скрытом режиме","Группа Красные блогеры" ,file=message_display )
	# while True:
	
	# print("Запуск парсинга",file=message_display)
	try:
		CB = Conteiner_Blogs(token,group_id, user_id)
		# CB.public_post()
	except:
		print(traceback.format_exc())
	finally:
		pass
		# print("Окончание цикла работы парсинга","Опубликовано {} постов" .format(CB.get_number_public_post()),file=message_display)

class MessageDisplay:
	def write(self, message):
		# print(type(message))
		if not (message==' ' or message=='\n') :os.system(' DISPLAY=:0 notify-send "{}"'.format(message))


if __name__ == '__main__':
	group_id =165089751 #чат-бот
	user_id= 117562096
	token = sys.argv[1]
	main(token, group_id, user_id)
	