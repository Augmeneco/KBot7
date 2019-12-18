import requests, os, re
from plugins.utils import *
from bs4 import BeautifulSoup

class main:
	level = 1
	keywords = ['что','чтоэто']
	def execute(self, msg):
		if len(msg['user_text']) > 0:
			exit()
		if 'photo' in msg['attachments'][0]:
			ret = msg['attachments'][0]['photo']['sizes']
			num = 0
			for size in ret:
				if size['width'] > num:
					num = size['width']
					url = size['url']
			index = requests.get('https://yandex.ru/images/search?url='+url+'&rpt=imageview').text
			soup = BeautifulSoup(index, 'html.parser')
			out = ''
			for tag in soup.find_all(class_='tags__tag'):
				out += '• '+tag.text+'\n'
			
			apisay('Я думаю на изображении что-то из этого: \n'+out,msg['toho'])
		else:
			apisay('Картинку сунуть забыл',msg['toho'])
