
url = 'https://vk.com/'
url_api ='https://api.vk.com/method/'
from time import sleep
# from smenaIP import requests_random_IP
# requests = requests_random_IP()
import requests
import os
# 

# user_id= 117562096
# group_id =165089751

class VkApi:
	def __init__(self, token,  api_version='5.84'):
		self.params={ 'access_token': token,'v':api_version}
		self.url_api ='https://api.vk.com/method/'
	def auth(self):
		pass
	def method(self,name_method , dict_method):
		sleep(5)
		dict_method.update(self.params)
		# print('name_method ',name_method)
		path_method = self.url_api+ name_method
		while True:
			if name_method in ('pages.save','wall.post'):
				r = requests.post(path_method,data=dict_method ).json()
			else:
				r = requests.get(path_method,params=dict_method ).json()
			if 'error' in r:
				print('error',r,'\nmethod',name_method, '\n dict',dict_method)
				Flood_control_error, Unknown_error = 9,1
				if r["error"]["error_code"] in (Flood_control_error, Unknown_error):
					sleep(60*10)
					continue
				return {'error':True, 'number_error':r["error"]["error_code"],'details':r}
			else:					
				return r['response']
			