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

class PostBlog():
	lp = None
	token,group_id, user_id = None, None, None
	
	def __init__(self,url,creator,token,group_id, user_id,chek=True):
		# Debug.__init__(self,chek=True)
		PostBlog.group_id = PostBlog.group_id or group_id
		PostBlog.user_id =  PostBlog.user_id or user_id
		PostBlog.lp = PostBlog.lp or Wrapper(Load_Post(group_id, user_id,token),True)
		self.url = url
		self.creator = creator
		self.list_link_post =self.get_list_data_for_public_bloger()
		self.lp.save_list_saves()
	
	@classmethod
	def count_public_post(cls):
		return cls.lp.return_count_puplic_post()

	@classmethod
	def clean_album(cls):
		cls.lp.clean()
	def function_load(self,url,title):
		raise Exception('Метод д/б определен в дочернем классе')
	def get_list_data_for_public(self,list_date,list_header,begining=1,end=None,list_urls=None):
		soup = BeautifulSoup(get_html(self.url), 'lxml')
		list_urls = list_urls or list_header
		print(list_urls, soup)
		return [(url.get('href'),head.text,date.text) 
			for (url,head,date) in 
				zip(soup.find_all(*list_urls)[begining:end],
					soup.find_all(*list_header)[begining:end],
					soup.find_all(*list_date)[begining:end]) ]
		
	def public_current_post(self, list_data):
		
		for url,head,date in list_data:
			name_post = "{}  от {}".format(' '.join(head.replace('"','').split()),date)
			name_post = head.replace('"','')
			if  not url in PostBlog.lp.list_saves:
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
		PostBlog.__init__(self,'https://onb2017.livejournal.com/?skip=50','ONB 2017',*args)
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
		list_blog =  Botya, #BlauKraeh, Ballaev, ONB, Remi, Bulgat,
		# list_blog  = Ballaev,
		self.blogers=[blog(*arg) for blog in list_blog]
	

class MonitoringLJ():
	def __init__(self,token,group_id, user_id):
		self.lp = Wrapper(Load_Post(group_id, user_id,token),True)
		# self.list_link_post =self.get_list_data_for_public_bloger()
			
	def __call__(self,dir_parser):
		try:
			list_public_post = self.get_list_posts(
									dir_parser['url'],
									dir_parser['list_date'],
									dir_parser['list_header'],
									dir_parser['list_urls'])
			# print(list_public_post)
			self.public_current_post(list_public_post,dir_parser['post'],dir_parser['creator'])
			self.lp.save_list_saves()
		except:
			print(traceback.format_exc())

	def get_list_posts(self,url,list_date,list_header,list_urls=None):
		soup = BeautifulSoup(get_html(url), 'lxml')
		list_urls = list_urls or list_header
		return [(url.get('href'),head.text,date.text) 
			for (url,head,date) in 
				zip(soup.find_all(*list_urls),
					soup.find_all(*list_header),
					soup.find_all(*list_date)) ]

	def public_current_post(self, list_public_post,parser_post,creator):
		for url,head,date in list_public_post:
			name_post = head.replace('"','')
			if  not url in self.lp.list_saves:
				self.function_load(url,head,parser_post,creator,date)
				self.lp.load_post(name_post,self.post_for_public,url)
	
	def load_post(self,url,title,soup,creator,date,prefix=''):
		if title:
			self.post_for_public = format_post(soup,prefix) + '\n[{}| {} от {}]'.format(url,creator,date)			

	def function_load(self,url,title,parser_post,creator,date): 
		soup = BeautifulSoup(get_html(url), 'lxml')
		# post =  soup.find(parser_post)
		post =  soup.find(attrs=parser_post)
		# print(soup,"---|||----",post, sep='\n')
		self.load_post(url,title,post,creator,date)
		return title


def main(token, group_id, user_id, creator='ALL',url_creator=None):

	try:
		1
		# CB = Conteiner_Blogs(token,group_id, user_id)
		# CB.public_post()
	except:
		print(traceback.format_exc())
	finally:
		pass
	
	# CC('https://onb2017.livejournal.com/?skip=30','ONB 2017', ONB_dir_parser,token,group_id, user_id)
	# CC(Remi_dir_parser,token,group_id, user_id)
	# Remi(token,group_id, user_id)



class MessageDisplay:
	def write(self, message):
		# print(type(message))
		if not (message==' ' or message=='\n') :os.system(' DISPLAY=:0 notify-send "{}"'.format(message))


if __name__ == '__main__':
	group_id = 165089751 #чат-бот
	user_id = 117562096
	token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
	# token = sys.argv[1]
	# main(token, group_id, user_id)
	'https://m.vk.com/page-165089751_54334503?api_view=f1f5957dfb1e6e4f65b8ff44f8dd15'

		# print("Окончание цикла работы парсинга","Опубликовано {} постов" .format(CB.get_number_public_post()),file=message_display)
	
	ONB_dir_parser = {
		'url':          'https://onb2017.livejournal.com/',
		'creator':      'ONB 2017',
		'list_date' : ('span',{'class':"date-entryunit__day"}),
		'list_header' : ('h3',{'class':"entryunit__head"}),
		'list_urls' : ('a',{'class':"entryunit__head"}),
		'soup':None,
		'post':{'class':'entry-content'},

	}
	
	Remi_dir_parser = {
		'url':'https://remi-meisner.livejournal.com/?skip=2',
		'creator':'Реми Майнсер',
		'list_header' : ('a', {'class':"subj-link"}),
		'list_date' :('abbr', {'class':"updated"} ),
		'list_urls':  None,
		'soup':None,
		'post':{'class':'entry-content'},

	}

	Ballaev = {
		'url':'https://p-balaev.livejournal.com/',
		'creator':'Петр Балаев',
		'list_header' : ('a',{'class':"subj-link"}),
		'list_date' :('abbr' ,{'class':"updated"}),
		'list_urls':  None,
		'soup':None,
		'post':{'class':'entry-content'},

	}

	Bulgat = {
		'url':'https://bulgat.livejournal.com/',
		'creator':'bulgat',
		'list_date' : ('abbr' ,{'class':"updated"}),
		'list_header' : ('dt', {'class':"entry-title"}),
		'list_urls' : ('a', {'class':"subj-link"}),
		'soup':None,
		'post':{'class':'entry-content'},

	}
	public_post = MonitoringLJ(token,group_id, user_id)
	# public_post.initial_creator(Remi_dir_parser)
	public_post(ONB_dir_parser)