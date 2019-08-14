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
		# self.get_list_data_for_public()
	@classmethod
	def count_public_post(cls):
		return cls.lp.return_count_puplic_post()
	def public_post (self):
		# second_in_day = 24*60*60
		# now_time = int(time.mktime(datetime.now().timetuple()))
		# next_day = int(time.mktime((date.today()+timedelta(days=1)).timetuple()))
		# time_public = lambda i: now_time+(next_day-now_time)//(i+1)
		# time_public = iter(range(now_time+15, next_day ,(next_day-now_time)//i))
		for url in self.list_link_post:
			try:
				name_post = 'Eror load post'
				name_post = "{}  от {}".format(self.function_load(url),datetime.now().strftime('%d-%m-%Y')
)
				# i = self.count_public_post()
				# print('time_public ', url, time_public(i))
				PostBlog.lp.load_post(name_post,self.post_for_public,url)#,time_public(i))
			except:
				print(traceback.format_exc())
				print(name_post , url, 'ошибка при сохранение, необходим обработчик данной ошибки')
		return self.count_public_post()
	@classmethod
	def clean_album(cls):
		cls.lp.clean()
	def function_load(self,url,title):
		raise Exception('Метод д/б определен в дочернем классе')
	def get_list_data_for_public(self,list_date,list_header,begining=1,end=None):
		soup = BeautifulSoup(get_html(self.url), 'lxml')
		# list_link_post = soup.find_all(*find_all)[begining:end]
		dates = [date.text for date in soup.find_all(*list_date)[begining:end]]
		headers = [head.text for head in soup.find_all(*list_header)[begining:end]]
		urls = [url.get('href') for url in soup.find_all(*list_header)[begining:end]]
		# print(list_link_date,list_link_post)
		# if find :list_link_post = [i.find(*find) for i in list_link_post]
		# list_link_post = [i.get('href') for i in list_link_post]
		return zip(urls,headers,dates)
		
	def public_current_post(self, list_data):
		for url,head,date in list_data:
			name_post = "{}  от {}".format(head,date)
			if  name_post not in PostBlog.lp.list_saves:
				self.function_load(url,head)
				PostBlog.lp.load_post(name_post,self.post_for_public,url)


		# return [url for url in list_link_post if url not in PostBlog.lp.list_saves ]
		# self.list_link_post = 
		# return len(self.list_link_post)
	
	def load_post(self,url,title,soup,prefix=''):
		if title:
			self.post_for_public = format_post(soup,prefix) + '\n[{}| {}]'.format(url,self.creator)			

class Bulgat(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://bulgat.livejournal.com/','bulgat',*args)
	def  get_list_data_for_public_bloger(self,begining=0):
		# find_all = ('a',{'class':"subj-link"})
		list_date = ('abbr' ,{'class':"updated"})
		list_header = ('dt', {'class':"entry-title"})
		# find = ()
		self.public_current_post(PostBlog.get_list_data_for_public(self,list_date,list_header,begining,2))
	def function_load(self,url,title):
		soup = BeautifulSoup(get_html(url), 'lxml')
		post = soup.find('div',class_='entry-content')
		# title = soup.find_all('dt', class_="entry-title")[-1].text
		self.load_post(url,title,post)
		# return title	

class BlauKraeh(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://blau-kraehe.livejournal.com/','Яна Завацкая',token,group_id, user_id)
	def  get_list_data_for_public_bloger(self,begining=None):
		begining = begining and begining+1
		find_all = ('h2', {'class':"asset-name page-header2"})
		find = ('a',{})
		list_date = ('abbr', {'class':"datetime"})
		list_header = ('a', {'class':"subj-link"})
		
		self.public_current_post(PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3))
		
	def function_load(self,url,title):
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		# title = soup.find('h1').text
		post = soup.find('article', class_="b-singlepost-body entry-content e-content")
		self.load_post(url,title,post)
		return title
class Botya(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://botya.livejournal.com/','botya',*args)
	def  get_list_data_for_public_bloger(self,begining=0):
		# find_all = ('div', {'class':"entryHolder"})
		# find = ('a',{'class':"subj-link"})
		list_date =('span',{'class':"entryHeaderDate"} )
		list_header= ('a', {'class':"subj-link"})
		self.public_current_post(
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3))
	def function_load(self,url,title): 
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		# title = soup.find('h1').text
		post = soup.find('article', class_="b-singlepost-body entry-content e-content")
		self.load_post(url,title,post)
		return title
class Ballaev(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://p-balaev.livejournal.com/','Петр Балаев',*args)
	def  get_list_data_for_public_bloger(self,begining=1):
		# print("get_list_data_for_public")
		# find_all = ('div', {'class':"entry-wrap js-emojis"})
		# find = ('a',{'class':"subj-link"})
		list_date = ('abbr' ,{'class':"updated"})
		list_header = ('a',{'class':"subj-link"})

		self.public_current_post(
			[(url,header,date) for (url,header,date) in 
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,8) 
			if ('https://p-balaev.livejournal'in url and 'Мои твиты' not in header)])
		# public_current_post(urls,headers,dates)
		# list_link_post=[]
		# for url in self.list_link_post:
		# 	if 'https://p-balaev.livejournal'in url:
		# 		title = BeautifulSoup(get_html(url), 'lxml').find_all('h4', {'class':"entry-title-text"})[-1].text
		# 		if 'Мои твиты' not in title :
		# 			list_link_post.append(url)
		# # self.list_link_post =  list_link_post[1:begining]
		# 		# print(len(self.list_link_post), self.list_link_post)
		# 		self.function_load(url,head)
		# 		PostBlog.lp.load_post(name_post,self.post_for_public,url)

		# return len(self.list_link_post)
	def function_load(self,url,title):
		soup = get_html(url)
		title = BeautifulSoup(soup, 'lxml').find_all('h4', {'class':"entry-title-text"})[-1].text
		title = title.split('entry')[0]
		post = BeautifulSoup(soup, 'lxml').find('div',class_='entry-content')
		self.load_post(url,title,post)
		return title
class ONB(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://onb2017.livejournal.com/','ONB 2017',*args)
	def  get_list_data_for_public_bloger(self,begining=1):
		find_all = ('link',{'itemprop':"url"})
		find = ()
		begining = begining and begining+1
		return PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3)
	def function_load(self,url,title): 
		soup = BeautifulSoup(get_html(url), 'lxml').find('div',class_='b-singlepost-wrapper')
		# title = soup.find('h1').text
		post = soup.find("div", class_="b-singlepost-bodywrapper")
		self.load_post(url,title,post)
		return title	
class Remi(PostBlog):
	def __init__(self,*args):
		PostBlog.__init__(self,'https://remi-meisner.livejournal.com/?skip=2',
			'Реми Майнсер',*args)
	def  get_list_data_for_public_bloger(self,begining=None):
		find_all = ('a',{'class':"summary-comments"})
		find = ()
		return PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3)
	def function_load(self,url,title): 
		soup =  BeautifulSoup(get_html(url), 'lxml')
		# title = soup.find_all('dt', class_="entry-title")[-1].text
		post = soup.find('div',class_='entry-content')
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
			PostBlog.get_list_data_for_public(self,list_date,list_header,begining,3)
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
		list_blog = (Botya,Remi,BlauKraeh,Class1957,Bulgat, Ballaev,ONB,)
		list_blog = Bulgat, Botya, BlauKraeh, Ballaev,
		self.blogers=[blog(*arg) for blog in list_blog]
		self.number_public_post = PostBlog.count_public_post()
	def public_post (self):
		for blog in self.blogers:
			pass
			# blog.get_list_data_for_public()
			# blog.public_post()
		self.blogers[0].clean_album()
	
	def get_number_public_post(self):
		return self.number_public_post




def main(token, group_id, user_id, creator='ALL',url_creator=None):
	
	message_display = MessageDisplay()
	print("Запуск парсинга, в скрытом режиме","Группа Красные блогеры" ,file=message_display )
	# while True:
	CB = Conteiner_Blogs(token,group_id, user_id)
	print("Запуск парсинга",file=message_display)
	try:
		CB.public_post()
	except:
		print(traceback.format_exc())
	finally:
		print("Окончание цикла работы парсинга","Опубликовано {} постов" .format(CB.get_number_public_post()),file=message_display)

class MessageDisplay:
	def write(self, message):
		# print(type(message))
		if not (message==' ' or message=='\n') :os.system(' DISPLAY=:0 notify-send "{}"'.format(message))


if __name__ == '__main__':
	group_id =165089751 #чат-бот
	user_id= 117562096
	token = sys.argv[1]
	main(token, group_id, user_id)
	