	
def debug_LJ():
	from initial_scraper import get_html
	from bs4 import BeautifulSoup
	url = 'https://onb2017.livejournal.com/'
	url = 'https://bulgat.livejournal.com/'
	find_all = ('div', {'class':"entry-wrap js-emojis"})
	find = ('a',{'class':"subj-link"})
	find_date = ('abbr' ,{'class':"updated"})
	list_header = ('h3', {'class':"entryunit__title"})
	list_date = ('span' ,{'class':"date-entryunit__day"})
	list_date = ('abbr' ,{'class':"updated"})
	list_header = ('dt', {'class':"entry-title"})
	return BeautifulSoup(get_html(url),'lxml')#.find_all(*list_header)


def debug_vk():
	from vk_api_my import VkApi 
	token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
	group_id = -165089751
	vk = VkApi(token)
	import time
	# # res =  vk.method('execute',
	# #  	{'code':
	# #  	'return API.wall.get(%s).items@.text+ API.wall.get(%s).items@.text;'%{"owner_id":-165089751, "count":2,"offset":0}%{"owner_id":-165089751, "count":2, "offset":2}
	# #  	 })
	'return API.photos.getAlbums({"owner_id":-165089751})'
	# {"owner_id":%d,"count":10,"filter":"postponed,all"}).items@.text;'%group_id})

	code = '''
		var current_album = API.photos.getAlbums({"owner_id":%d,"count":1}).items[0];
		if (current_album.size>9000)
			{return current_album.id;}
		return API.photos.createAlbum({"owner_id":%d,"title":"альбом для фотографий %s","upload_by_admins_only":1}).id;
	'''%(-group_id, group_id, time.strftime("от %d %m %Y",time.gmtime()))
	return vk.method('execute',{'code':code})

if __name__ == '__main__':
	# res = debug_vk()
	soup = debug_LJ()#Оргии влиятельных миллионеров\n  от August 12th, 2019