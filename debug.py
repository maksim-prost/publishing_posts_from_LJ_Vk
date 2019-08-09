from vk_api_my import VkApi 

token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'

vk = VkApi(token)

res =  vk.method('execute',
 	{'code':
 	'return API.wall.get(%s).items@.text+ API.wall.get(%s).items@.text;'%{"owner_id":-165089751, "count":2,"offset":0}%{"owner_id":-165089751, "count":2, "offset":2}
 	 })
vk.method('execute',{'code':'return '+'+'.join(map(lambda s: 'API.wall.get({"offset":%s,"owner_id":%d}).items@.text'%(s,owner_id), range(0,200,100)))+';'})

"return API.wall.get({'owner_id': -165089751, 'offset': 0, 'count': 2}).items@.text+ API.wall.get({'owner_id': -165089751, 'offset': 2, 'count': 2}).items@.text;"
'return API.wall.get({"offset": 0, "owner_id": -165089751, "count": 2}).items@.text+ API.wall.get({"offset":2,"owner_id":-165089751,"count":2}).items@.text''