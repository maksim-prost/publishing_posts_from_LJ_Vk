import pytube
import re

def sub_all(pattern, simv_zam, string):
	temp = re.sub(pattern, simv_zam,str(string),re.DOTALL)
	while string != temp:
			string = temp
			temp = re.sub(pattern, simv_zam,str(string),re.DOTALL)
	return string

def format_post(page, prefix=''):
	"""
	функция удаляет html-разметку,
	сохраняя ссылки, изображения, видео, форматирование текста
	"""
	temp_string= str(page)
	link = lambda url: '' if not url else url if str(url).startswith('http') else prefix + url
	
	for  img in page.find_all('img'):
		# print(link(img.get('src')))
		temp_string =temp_string .replace(str(img),'\nimg {}\n'.format(link(img.get('src'))))
	
	for a in page.find_all('a'):
			temp_string  = temp_string .replace(str(a),'[{}|{}]'.format(link(a.get('href')),a.text))

	for video in page.find_all('iframe'):
		try:
			src = video.get('src')
			print(src)
			mo = re.search(r'vid=([0-9A-Za-z_-]{11})&',src) # r'(?:v=|\/)([0-9A-Za-z_-]{11})' - форрмат ссылки ютюбф
			if not mo: mo = re.search(r'embed/([0-9A-Za-z_-]{11})',src)
			# if not mo: mo = re.search(r'([0-9A-Za-z_-]{11})',src)
			print(mo.group(1))
			link_video ='https://www.youtube.com/watch?v=' +  mo.group(1)  
			try:	
				yt = pytube.YouTube(link_video)
				title = yt.title.replace(' ','_')
			except:
				title = 'Some_videos'
			shablon = '\nvideo {} {}\n'.format(link_video,title)
		except:
			shablon = '\n {} Some_videos '.format(src)
		temp_string =temp_string .replace(str(video),shablon)#'.'.join((yt.title,yt.streams.first().subtype))+'\n\n\n')

	for style in page.find_all('span'):
		if style.get('style') and 'vertical-align: super'in style.get('style'):
			# print(style.get('style'))
			temp_string =temp_string .replace(str(style),'{{sup}}'+style.text+'{{/sup}}')
	 
	for tag in ('b','gray','i','sub', 'sup','tt','code','br/','strike'):
		temp_string =  temp_string.replace('<'+tag+'>','{{'+tag+'}}').replace('</'+tag+'>','{{/'+tag+'}}')

	# for strike in page.find_all('strike'): 
	# 		temp_string =temp_string .replace(str(strike),'{{s}}'+strike.text+'{{/s}}')
	
	temp_string = sub_all(r'<div.*?>','\n',temp_string)
	temp_string = sub_all(r'<p.*?>','\n',temp_string)
	temp_string = sub_all(r'<.*?>','',temp_string)
	temp_string = sub_all(r'(\s*\n){2,}','\n',temp_string)
	temp_string = temp_string.replace('{{','<').replace('}}','>').replace('[|]','').replace('strike','s')	
	# print(temp_string)
	return temp_string
