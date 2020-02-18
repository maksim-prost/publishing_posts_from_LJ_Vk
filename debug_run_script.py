import os
import vk_api_my as vk_api
# help(os)
# os.system('./get_data_from_LJ_class.py' )
MAIN_ALBUM = 260894583
СURENT_VIDEO_ALBUM = 4793
СURENT_VIDEO_ALBUM = 4838
#   165089751 117562096 >>std.ou ')
token = '9a3e3c787c27cdcffb50046fb31b70c4dbb6e1b78dacb8a91d7e1a6e28d6041731d6918fb84822f54483d'
group_id = 165089751 #чат-бот
user_id = 117562096

# vk_user = vk_api.VkApi(token ,api_version='5.92')
# vk_user.auth()
# vk_user.method('photos.getUploadServer',
# 		{'group_id':group_id ,'album_id':album_id})["upload_url"]
# 		ur = vk_api.requests.post(upload_url, files = {'file1': file})
os.system('./get_data_from_LJ_class.py %s '%token)