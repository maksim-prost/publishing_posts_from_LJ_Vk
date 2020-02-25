#! ../venv/bin/python
#! /usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import os, sys

import traceback
from datetime import datetime, date, timedelta
import time
from format_html import format_post
from load_post_vk_class import Load_Post 
from load_image import get_html




class Wrapper:
	def __init__(self, object, chek=True):
		self.wrapper = object
		self.chek = chek
		
	def __getattr__(self,attrname):
		if self.chek: print(self.wrapper.__class__.__name__,  attrname)
		return getattr(self.wrapper, attrname)



'''class Class1957():
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
'''

		
class MonitoringLJ():
	def __init__(self,token,group_id, user_id):
		self.lp = Wrapper(Load_Post(group_id, user_id,token),True)
			
	def __call__(self,dir_parser):
		try:
			list_public_post = self.get_list_posts(
									dir_parser['url'],
									dir_parser['list_date'],
									dir_parser['list_header'],
									dir_parser['list_urls'])
			self.public_current_post(list_public_post,dir_parser['soup'],dir_parser['post'],dir_parser['creator'])
			self.lp.save_list_saves()
		except:
			print('Обработка ошибок')
			print(traceback.format_exc())

	def get_list_posts(self,url,list_date,list_header,list_urls=None):
		soup = BeautifulSoup(get_html(url), 'lxml')
		list_urls = list_urls or list_header
		return [(url.get('href'),head.text,date.text) 
			for (url,head,date) in 
				zip(soup.find_all(*list_urls),
					soup.find_all(*list_header),
					soup.find_all(*list_date)) ]

	def public_current_post(self, list_public_post,parser_soup,parser_post,creator):
		for url,head,date in list_public_post:
			name_post = head.replace('"','')
			if  not url in self.lp.list_saves:
				self.function_load(url,head,parser_soup,parser_post,creator,date)
				self.lp.load_post(name_post,self.post_for_public,url)
	
	def load_post(self,url,title,soup,creator,date,prefix=''):
		if title:
			self.post_for_public = format_post(soup,prefix) + '\n[{}| {} от {}]'.format(url,creator,date)			

	def function_load(self,url,title,parser_soup,parser_post,creator,date): 
		print(url,title,parser_post,creator,date)
		soup = BeautifulSoup(get_html(url), 'lxml')
		if parser_soup:
			soup =  soup.find(attrs=parser_soup)
		print(parser_soup,soup)
		post =  soup.find(attrs=parser_post)
		# print(soup,"---|||----",post, sep='\n')
		self.load_post(url,title,post,creator,date)
		return title



class MessageDisplay:
	def write(self, message):
		if not (message==' ' or message=='\n') :os.system(' DISPLAY=:0 notify-send "{}"'.format(message))


if __name__ == '__main__':
	from blogers import *
	import configparser  # импортируем библиотеку

	config = configparser.ConfigParser()  # создаём объекта парсера
	config.read("conf.ini")  # читаем конфиг
	token = config["VK"]['token']
	print(token)
	group_id = int(config["VK"]['group_id'])
	user_id = int(config["VK"]['user_id'])
	public_post = MonitoringLJ(token,group_id, user_id)
	public_post(ONB)
	public_post(Remi)
	public_post(Botya)
	public_post(Bulgat)
	public_post(BlauKraeh)
	public_post(Ballaev)