import requests
from plugins.utils import *

class main:
	level = 1
	keywords = ['кончи','кончил','cum']
	def execute(self, msg):
		if 'photo' in msg['attachments'][0]:
			ret = msg['attachments'][0]['photo']['sizes']
			num = 0
			for size in ret:
				if size['width'] > num:
					num = size['width']
					url = size['url']
			pic = requests.get('http://lunach.ru/?cum=&url='+url).content
			apisay('Готово!',msg['toho'],photo=pic)
		else:
			apisay('Картинку забыл сунуть',msg['toho'])