import random, requests
from plugins.utils import *

class main:
	level = 1
	keywords = ['rip','рип']
	def execute(self, msg):
		if msg['user_text'] == '':
			apisay('Текст то напиши',msg['toho'])
			exit()
		out = ''
		if len(msg['user_text'].split(' ')) > 70:
			apisay('Сообщение слишком больше, я не хочу чтобы яндекс наказали меня :(',msg['toho'])
			exit()
		for word in msg['user_text'].split(' '):
			result = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key='+msg['config']['yandex_key']+'&lang=ru-ru&text='+word).json()
			if len(result['def']) != 0:
				out += result['def'][0]['tr'][random.randint(0,len(result['def'][0]['tr'])-1)]['text']+' '
			else:
				out += word+' '
		apisay(out,msg['toho'])