from initial_scraper import get_html
from bs4 import BeautifulSoup	


def debug_LJ(url, scraper):
	return BeautifulSoup(get_html(url),'lxml').find_all(scraper)


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
	
	scraper = ('div',{'class':'entry-content'})
	url=         'https://onb2017.livejournal.com/'
	creator=     'ONB 2017'
	list_header = ('a', {'class':"subj-link"})
	list_date= ('span' ,{'class':"date-entryunit__day"})
	list_urls=    ('link',{'itemprop':"url"})
	soup=       ('div',{'class':'b-singlepost-wrapper'})
	post=        { "class":"b-singlepost-bodywrapper"}


	list_header = ('span',{'class':"j-w-entry-subject"})
	list_date = ('span',{'class':"date-entryunit__day"})
	list_urls = ('a',{'class':"j-w-comments-count"})
	soup = BeautifulSoup(get_html(url),'lxml')

'''
</li></ul></div><header class="entryunit__head"><h3 class="entryunit__title">
<a href="https://onb2017.livejournal.com/210025.html">А как насчет такого жилья в отличном районе и за умеренную цену?</a>
</h3>
</header><div class="entryunit__body">
<div class="entryunit__text">


<span class="date-entryunit__day">14 февраля 2020</span>

'''