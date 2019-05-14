# from load_post_vk_class import get_html
from PIL import Image, ImageFont,ImageDraw
from io import BytesIO, BufferedReader
import requests
import traceback

def get_html(url, stream = False):
	if stream: return requests.get(url, stream = True)
	return requests.get(url).text

def create_img_for_title(text):
	'''
	создает изображение для поста без картинок
	'''
	size_img =  (600, 400)
	font= ImageFont.truetype(font='Red_October_Stencil.ttf',size=26)
	list_text=[text]
	while True:
		size_text = font.getsize(list_text[-1])
		if size_text[0]<=size_img[0]:break
		list_text[-1:] = list_text[-1].split(maxsplit=size_text[0]//size_img[0])
	i=0
	while i<len(list_text)-1:
		if  font.getsize(list_text[i]+list_text[i+1])[0]+1<=size_img[0]:
			list_text[i] = list_text[i] +" "+ list_text[i+1]
			del(list_text[i+1])
		else: i += 1
	size_text = list(font.getsize( max(list_text, key=len)))
	size_text[1]=size_text[1]*len(list_text)
	text='\n '.join(list_text)
	img = Image.new("RGB",size_img, "#ff3319")
	draw = ImageDraw.Draw(img)
	draw.text(list(map(lambda x,y:(x-y)/2,size_img,size_text)),text, fill='yellow', font=font)
	# img_id, *temp = load_img_PIL(None,albom_id,img)
	return img
	# return img_id

def load_img(src,img):
	try:
		if src:
			# src = src.split('?')[0]
			# print('src',src)
			data = bytearray()
			for chunc in get_html(src,True).iter_content(1024):
				data+=chunc
			# print('load')
			file = BytesIO (data)
			# print('file')
			image = Image.open(file)
			format_ =  image.format
		if img:
			image = img
			format_ = 'PNG'
		
		file = BytesIO ()
		image.save(file, format_)

		file.name = 'img.{}'.format(format_)
		file = BufferedReader(file)
		file.seek(0)
		size = lambda w,h:( 610, int(610*h/w))
		size = size(*image.size)
		print(*size)
		# image.close()
		return file, size
	except:
		print('Error load image durring in server',src) #,albom_id)
		print(traceback.format_exc())
		return None, (None,None)
