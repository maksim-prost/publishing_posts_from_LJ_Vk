from vk_api_my import VkApi 
from initial_scraper import get_html
from bs4 import BeautifulSoup
url = 'https://p-balaev.livejournal.com/'
find_all = ('div', {'class':"entry-wrap js-emojis"})
find = ('a',{'class':"subj-link"})
		
soup = BeautifulSoup(get_html(url),'lxml')

# token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
# group_id = -165089751
# vk = VkApi(token)

# # res =  vk.method('execute',
# #  	{'code':
# #  	'return API.wall.get(%s).items@.text+ API.wall.get(%s).items@.text;'%{"owner_id":-165089751, "count":2,"offset":0}%{"owner_id":-165089751, "count":2, "offset":2}
# #  	 })
	
# res = vk.method('execute',
			# {'code':
			# 'return API.wall.get({"owner_id":%d,"count":100,"filter":"postponed"}).items@.text;'%group_id})
		