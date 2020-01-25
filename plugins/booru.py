import random, requests, xmltodict, traceback, time
from plugins.utils import *

class main:
	level = 1
	keywords = ['арт','хентай','art','hentai','бура','booru']
	def execute(self, msg):
		count = 10
		needtag = False
		if '-tags' in msg['user_text']:
			msg['user_text'] = msg['user_text'].replace(' -tags ','').replace(' -tags','')
			needtag = True
		if msg['user_text'].split(' ')[0].isdigit():
			count = int(msg['user_text'].split(' ')[0])
			if count <= 0: count = 1
			if count > 10 and msg['userinfo'][1] < 2:
				apisay('Обычный пользователь не может больше 10 артов за раз, тебе нужон второй ранг :(',msg['toho'])
				count = 10
			query = ' '.join(msg['user_text'].split(' ')[1:]).replace(' ','+')
		else:
			query = msg['user_text'].replace(' ','+')
		imgs = []
		
		result = requests.get('https://safebooru.org/index.php?page=dapi&s=post&q=index&limit=1000&tags='+query).text
		result = json.loads(json.dumps(xmltodict.parse(result)))['posts']
		if 'post' not in result:
			apisay('Ничего не найдено :(',msg['toho'])
			return 0
		if len(result['post']) < count:
			count = len(result['post'])
		tags = '{0} мс\n({1}/{2})\nВсе теги: '
		i = 0
		posts = list(range(len(result['post'])))
		nums = []
		while i != count:
			randnum = random.choice(posts)
			if randnum not in nums:
				nums.append(randnum)
				i += 1
		params = {'access_token':msg['config']['group_token'],'v':'5.103','type':'typing','peer_id':msg['toho']}
		for i in nums:
			url = result['post'][i]['@file_url']
			tags += result['post'][i]['@tags']
			requests.post('https://api.vk.com/method/messages.setActivity',data=params)
			imgs.append(requests.get(url).content)
		timer = time.time()
		imglist = list(chunks(imgs,10))
		for imgs in imglist:
			requests.post('https://api.vk.com/method/messages.setActivity',data=params)
			apisay(' ',msg['toho'],photo=imgs)
		if needtag:
			tags = tags.format(time.time()-timer,count,len(result['post']))
			apisay(tags,msg['toho']) 