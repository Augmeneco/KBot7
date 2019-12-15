import random, requests, re
from plugins.utils import *

class main:
	level = 1
	keywords = ['двач','2ch','сосач','харкач']
	def execute(self, msg):
		if msg['user_text'] == '': msg['user_text'] = 'b'
		try:
			thread = requests.get('https://2ch.hk/'+msg['user_text']+'/'+str(random.randint(0,9)).replace('0','index')+'.json').json()['threads']
		except:
			apisay('Такой борды не существует',msg['toho'])
			return 0
		thread = thread[len(thread)-1]
		url = 'https://2ch.hk/'+msg['user_text']+'/res/'+thread['posts'][0]['num']+'.html'
		text = 'Оригинал: '+url+'\n'+re.sub('(\<(/?[^>]+)>)','',thread['posts'][0]['comment'])
		img = 'https://2ch.hk'+thread['posts'][0]['files'][0]['path']
		img = requests.get(img).content
		apisay(text, msg['toho'],photo=img)