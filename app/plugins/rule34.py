import random, requests, untangle, traceback, time
from plugins.utils import *

class main:
	level = 1
	keywords = ['34','р34','r34','rule34','хентай']
	def execute(self, msg):
		blacklist = '-anthro+-fur+-scat*+-darling_in_the_franxx+-furry+-dragon+-guro+-animal_penis+-animal+-wolf+-fox+-webm+-my_little_pony+-monster*+-3d+-animal*+-ant+-insects+-mammal+-horse+-blotch+-deer+-real*+-shit+-everlasting_summer+-copro*+-wtf+'
		timer = time.time()
		try:
			parse = untangle.parse(requests.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=1000&tags='+blacklist+msg['user_text'].replace(' ','+')).text)
		except:
			apisay('Что-то не так :(\n\n'+traceback.format_exc(),msg['toho'])
			return 0
		if int(parse.posts['count']) > 0:
			if len(parse.posts.post) == 0:
				mess = 'Дрочевня подкатила ('+str(time.time()-timer)+' sec)\n(1/1)\n----------\nОстальные теги: '+parse.posts.post['tags']
				parse = parse.posts.post['file_url']
			else:
				randnum = random.randint(0,len(parse.posts.post))
				mess = 'Дрочевня подкатила ('+str(time.time()-timer)+' sec)\n('+str(randnum)+'/'+str(len(parse.posts.post))+')\n----------\nОстальные теги: '+parse.posts.post[randnum]['tags']
				parse = parse.posts.post[randnum]['file_url']
			pic = requests.get(parse).content
			apisay(mess,msg['toho'],photo=pic)
		else: apisay('Ничего не найдено :(',msg['toho'])