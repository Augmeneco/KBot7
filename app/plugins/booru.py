import random, requests, untangle, traceback, time
from plugins.utils import *

class main:
	level = 1
	keywords = ['арт','хентай','art','hentai','бура','booru']
	def execute(self, msg):
		#proxies = {'http': 'socks5h://localhost:9050','https': 'socks5h://localhost:9050'}
		timer = time.time()
		try:
			parse = untangle.parse(requests.get('https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1000&tags='+msg['user_text'].replace(' ','+')).text)
		except:
			apisay('Что-то не так с прокси :(\n\n'+traceback.format_exc(),msg['toho'])
			return 0
		if int(parse.posts['count']) > 0:
			randnum = random.randint(0,len(parse.posts.post))
			mess = 'Бурятские артики ('+str(time.time()-timer)+' sec)\n('+str(randnum)+'/'+str(len(parse.posts.post))+')\n----------\nОстальные теги: '+parse.posts.post[randnum]['tags']
			parse = parse.posts.post[randnum]['file_url']
			pic = requests.get(parse).content
			apisay(mess,msg['toho'],photo=pic)
		else: apisay('Ничего не найдено :(',msg['toho'])