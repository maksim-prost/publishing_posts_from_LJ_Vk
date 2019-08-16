# import requests
import vk_api_my as vk_api

import os
import time
from datetime import date
import traceback

import time, datetime
from load_image import create_img_for_title, load_img
# from connection_db import InteractionWithDB
# from smenaIP import requests_random_IP
MAIN_ALBUM = 260894583
СURENT_VIDEO_ALBUM = 4793
СURENT_VIDEO_ALBUM = 4838
class Load_Post():
	def __init__(self,group_id_, user_id_,token):
		self.vk_user = vk_api.VkApi(token ,api_version='5.92')
		self.vk_user.auth()
		global vk_user, group_id, user_id
		group_id, user_id = group_id_, user_id_
		self.group_id, self.user_id = group_id, user_id
		vk_user = self.vk_user
		# self.connection_db = InteractionWithDB()
		self.count_puplic_post = self.load_count_puplic_post()#connection_db.count_today_posts()
		self.album_id = self.get_curent_album()  
		self.album_video_id = СURENT_VIDEO_ALBUM
		self.load_list_saves()
	def get_curent_album(self):
		code = '''
			var current_album = API.photos.getAlbums({"owner_id":%d,"count":1}).items[0];
			if (current_album.size<9000)
				{return current_album.id;}
			return API.photos.createAlbum({"owner_id":%d,"title":"альбом для фотографий %s","upload_by_admins_only":1}).id;
		'''%(-group_id, group_id, time.strftime("от %d %m %Y",time.gmtime()))
		return self.vk_user.method('execute',{'code':code})
		return MAIN_ALBUM
		album_id = self.connection_db.curent_album_id()
		
		return album_id

	def clean (self):
		return
		# vk_user = self.vk_user
		# clean(self.group_id, self.connection_db.list_album_id())	
	
	def load_list_saves(self):
		#gjследние 300 публикацмй на странице
		self.list_saves = self.vk_user.method('execute',
			{'code':
			'return %s;'%'+'.join(map(lambda s: 'API.wall.get({"offset":%s,"owner_id":%d,"count":100}).items@.text'%(s,-group_id), range(0,300,100)))})
		self.list_saves.extend(self.vk_user.method('execute',
			{'code':
			'return API.wall.get({"owner_id":%d,"filter":"postponed"}).items@.text;'%-group_id}))
		print(len(self.list_saves))

	def load_count_puplic_post(self):
		current_day = int(time.mktime((date.today()).timetuple()))
		self.list_public_post = self.vk_user.method('execute',
			{'code':
			'return API.wall.get({"owner_id":%d,"count":50}).items@.date;'%(-group_id)})
		self.list_public_post.reverse()
		return len([i for i in self.list_public_post if int(i)>current_day])
	
	def load_post(self,title_post,post_for_public,link,repost_id=None):
		if self.count_puplic_post>50:
			raise Exception('Превышено ограничение на 50 публикаций в сутки')
		global  time_puplic
		time_interval = int(60*60*24/50)#ограничение на 50 публикаций в сутки
		time_puplic = int(time.time())
		if self.list_public_post[-1]>time_puplic:
			time_puplic = self.list_public_post[-1]
		time_puplic += time_interval
		self.list_public_post.append(time_puplic)
		album_id,albom_video_id,group_id= self.album_id ,self.album_video_id, self.group_id
		dict_img = []
		text=[]
		for line in post_for_public.split('\n'):
			marker, *content = line.split(' ')
			if marker=='img':
				src = content[0].strip()
				image_id,width,height = load_img_PIL(src,album_id)
				line = '\n[[photo-{}_{}|{}x{}px| ]]\n'.format(group_id,image_id,width,height)
				dict_img.append('photo-{}_{}'.format(group_id,image_id))

			elif marker=='video':
				vk_link_video = load_video(*content[:2],albom_video_id)
				line ='\n<center>[[{}|600x400px;player| ]]</center>\n'.format(vk_link_video)
				dict_img.append(vk_link_video)
			text.append(line+'\n')
		
		if post_wiki_page(title_post,text,dict_img,album_id,repost_id):
			self.count_puplic_post += 1
			# self.connection_db.uppdate_link((link,))
		# clean_empty_album(albom_video_id,album_id)
	
	def return_count_puplic_post(self):
		return self.count_puplic_post
	
def load_img_PIL(src,album_id,img=None):
	rez = ' ',' ',' '
	file, size = load_img (src,img)
	if not file: return rez
	try:
		upload_url=vk_user.method('photos.getUploadServer',
		{'group_id':group_id ,'album_id':album_id})["upload_url"]
		ur = vk_api.requests.post(upload_url, files = {'file1': file})
		ur = ur.ok and ur.json() 
		# print('ur-',ur)
		if ur:
			img_id =  vk_user.method('photos.save',
			{'group_id':group_id,'server':ur['server'],'album_id':album_id,
						'photos_list':ur['photos_list'],'hash':ur['hash']})[0]['id']
			# print(img_id)
			rez =  img_id, *size#.split('_')[1], *size
	except:
		print(traceback.format_exc())
		print('Error load image durring process VK')
	finally:
		file.close()
	return rez

def get_albom_id(name_albom):
	album_image_id,album_video_id = MAIN_ALBUM, 91
	try:
		r = vk_user.method('photos.createAlbum',{ 'title':name_albom,'group_id':group_id} )
	except:
		r = {"aid": album_image_id, "owner_id": -group_id}
	try:
		v = vk_user.method('video.addAlbum',{ 'title':name_albom,'group_id':group_id} )
	except:
		v = {'album_id': album_video_id}
	# print(r,v,sep='\n')
	return r["aid"],v['album_id'],-r["owner_id"]

def load_foto(path_foto,albom_id):

	upload_url=vk_user.method('photos.getUploadServer',
			{'group_id':group_id ,'album_id':albom_id})["upload_url"]
	
	with open(path_foto, 'rb') as foto:	
		ur = vk_api.requests.post(upload_url, files = {'file1': foto}).json() 
		# foto.close()
	img =vk_user.method('photos.save',
	 		{'group_id':group_id,'server':ur['server'],'album_id':albom_id,
	 					'photos_list':ur['photos_list'],'hash':ur['hash']})
	# time.sleep(2)
	return group_id,img[0]['id']

def load_video(url_video,about_video,albom_id):
	r = vk_user.method('video.save',
			{'group_id':group_id ,'album_id':albom_id,
			 'name':about_video, 'link':url_video})
	upload_url = r["upload_url"]
	id_video = r['vid']
	# print('\n id_video \n', id_video)
	r = vk_api.requests.get(upload_url)

	return 'video-{}_{}'.format(group_id,id_video,'')	
	return 'Возникли ошибки при загрузки  видео \n{}'.format(url_video)

def split_wiki(text,name_wiki,number_chunc):
	# print(text)
	# print(len(text), number_chunc)
	wiki = text.split('\n')
	N = len (wiki)
	part_string_in_chunc = N//number_chunc +1 
	# print(N, part_string_in_chunc)
	k = zip(range(0,N,part_string_in_chunc), range(part_string_in_chunc,N+part_string_in_chunc,part_string_in_chunc))
	# print(list(k))
	for z,(i,j) in enumerate(k):
		sufics = '\n[[{}{} | Читать дальше..]]'.format((z+1)*'+',name_wiki) if z<number_chunc-1 else ''
		yield '\n'.join(wiki[i:j]) + sufics

def post_wiki_page(title,text,dict_img,albom_id,repost_id):
	# print('wiki page, albom_id', albom_id)
	from format_html import sub_all
	url = text[-1]
	text = ''.join(text)
	text_message = '\n'.join([title])#+url.replace(']','').replace('[','').split('|'))
	number_char = len(text)
	if number_char < 16380:
		id_wiki_page =vk_user.method('pages.save',{'text':text , 'group_id': group_id, 'title':title})
	else:
		title = title.replace('"','')
		for i,chunc in enumerate(split_wiki(text,title,number_char//10000 +1)):
			# print(i,chunc, sep='\n')
			temp = vk_user.method('pages.save',
				{'text':chunc, 'group_id': group_id, 'title':'+'*i + title}) 
			if not i: id_wiki_page = temp
	# print('dict_img',dict_img)
	for photo_or_video in dict_img:
		# print(photo_or_video)
		if 'photo' in photo_or_video: break
	else:
		# print(title)
		img_id, *temp = load_img_PIL(
			False,albom_id,
			create_img_for_title(title.replace('»','"').replace('«','"')))
		dict_img.insert(0,'photo-{}_{}'.format(
			group_id,img_id))
	# print('page{}_{},'
			# .format(-group_id,id_wiki_page) + ','.join(dict_img[:1]))
	post = vk_user.method('wall.post',
		{"owner_id":-group_id,'from_group':1, 'message': text_message,'publish_date':time_puplic,
		'attachments':'page{}_{},'
			.format(-group_id,id_wiki_page) + ','.join(dict_img[:1])})
	if post.get('error'): print(post['details'])
	return not post.get('error')
	# print('exit wiki page')

def clean_empty_album(albom_video_id,albom_id):
	try:
		count =vk_user.method('video.getAlbumById',{"owner_id":-group_id,'album_id':albom_video_id})['count']
		if not count: vk_user.method('video.deleteAlbum',{'group_id':group_id,'album_id':albom_video_id})
	except:
		print("Не удалось обработать альбом с видео {}, после публикации поста".format(albom_video_id))
	try:
		count =vk_user.method('photos.get',{"owner_id":-group_id,'album_id':albom_id})
		if not len(count): vk_user.method('photos.deleteAlbum',{'group_id':group_id,'album_id':albom_id})
	except:
		print("Не удалось обработать альбом с фотографиями {}, после публикации поста".format(albom_id))

def clean_wall_from_albums(group_id,list_album_id,
			type_album="photos.getAlbums",type_delete='photos.deleteAlbum',aid='aid'):
	# "photos.getAlbums" 'video.getAlbums' video.deleteAlbum photos.deleteAlbum
	count_albums = vk_user.method(type_album,
		{"owner_id":-group_id, "offset":50, "count":100})
	i=1
	while len(count_albums)>1:
		for album in count_albums[1:]:
			if album[aid] not in list_album_id:
				vk_user.method(type_delete,{'group_id':group_id,'album_id':album[aid]})
		count_albums = vk_user.method(type_album,
		{"owner_id":-group_id, "offset":100*i, "count":100})
		i+=1

def clean(group_id,list_album_id):
	clean_wall_from_albums(group_id,list_album_id,'video.getAlbums','video.deleteAlbum','album_id')
	clean_wall_from_albums(group_id,list_album_id)

def template_clean_albom(group_id,type_album, type_count, type_delete):
	list_title_albom = []
	for album in vk_user.method(type_album,{"owner_id":-group_id,'count':100})['items']:
		count =vk_user.method(type_count,{"owner_id":-group_id,'album_id':album['id']})['count']
		if album['title'] not in list_title_albom:
			list_title_albom.append(album['title'])
		else: count = False #удфляем альбом если такое название уже существует
		print(album,count)
		if not count:
			vk_user.method(type_delete,{'group_id':group_id,'album_id':album['id']})

def wall_clean():
	for post in vk_user.method('wall.get',{"owner_id":-group_id,'count':100})['items']:
		# print(post['id'])
		vk_user.method('wall.delete',{'group_id':group_id,'post_id':post['id']})

def main():
	
	global  vk_user, login, password ,group_id, user_id
	group_id =165089751 #чат-бот
	user_id= 117562096
	# vk_user = vk_register()
	template_clean_albom(group_id,'video.getAlbums','video.getAlbumById','video.deleteAlbum')
	template_clean_albom(group_id,'photos.getAlbums','photos.get','photos.deleteAlbum')
	return 


if __name__ == '__main__':
	main()