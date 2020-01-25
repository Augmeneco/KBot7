import json, os, requests, re
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from plugins.utils import *

class main:
	level = 1
	keywords = ['цитген','citgen','quote','цитата']
	def execute(self,msg):
		def wrapper(s, length):
			lines = list()
			for line in s.split('\n'):
				lines.append(str())
				for token in re.split(r'(\s*)(\S+)', line):
					if len(token)+len(lines[-1]) > length:
						if re.match(r'\s*', token).span()[1] == len(token):
							lines[-1] += token[:length-len(lines[-1])-1]
							token = token[length-len(lines[-1])-1:]
						lines.extend([token[i:i+length] for i in range(0, len(token), length)])				
					else:
						lines[-1] += token
			return lines
		
		for font in ['Roboto-Regular.ttf','Roboto-Medium.ttf']:
			if font not in os.listdir('/tmp/'):
				ret = requests.get('https://github.com/Augmeneco/KBot5/blob/master/data/'+font+'?raw=true').content
				open('/tmp/'+font,'wb').write(ret)
		
		img = Image.new('RGB', (800,10000), color = (0,0,0))
		
		if 'reply_message' in msg:
			message = msg['reply_message']
			usertext = message['text']+'\n'
		else:
			if len(msg['fwd_messages']) == 0: 
				apisay('Ты забыл переслать сообщение :(',msg['toho'])
				return 0
			message = msg['fwd_messages'][0]
			usertext = ''
			for i in msg['fwd_messages']:
				usertext += i['text']+'\n'
			
		
		
		if message['from_id'] < 0:
			user_info = requests.post('https://api.vk.com/method/groups.getById',data={'access_token':msg['config']['group_token'],'v':'5.90','group_ids':message['from_id']*-1}).json()['response'][0]
			name = user_info['name']
		else:
			user_info = requests.post('https://api.vk.com/method/users.get',data={'access_token':msg['config']['group_token'],'v':'5.90','fields':'photo_200','user_ids':message['from_id']}).json()['response'][0]
			name = user_info['first_name']+' '+user_info['last_name']

		ava = user_info['photo_200']
		ava = requests.get(ava,stream=True).raw
		ava = Image.open(ava)
	
		title = ImageFont.truetype('data/title.ttf', 40) 
		author = ImageFont.truetype('data/author.ttf', 30) 
		content = ImageFont.truetype('data/text.ttf', 35) 

		draw = ImageDraw.Draw(img)
		text_w, text_h = title.getsize('Цитаты великих людей')
		img_w, img_h = img.size;
		draw.text(((img_w-text_w)/2,text_h),'Цитаты великих людей',fill='white',font=title)

		img.paste(ava,[text_h,text_h*3])

		symbol_w = content.getsize('а')[0]

		offset_h = 10
		for wrap in wrapper(usertext,int((800-(text_h+210))/symbol_w)):
			draw.text((text_h+210,text_h*3+offset_h),wrap,fill='white',font=content)
			offset_h += text_h
		
		draw.text((text_h+210,text_h*3+offset_h),'(c)'+name,fill='white',font=author)
		offset_h += text_h
		
		if text_h*3+offset_h+10 < text_h*3+200+text_h:
			img = img.crop([0,0,800,text_h*3+200+text_h])
		else:
			img = img.crop([0,0,800,text_h*3+offset_h+10])
		imgByteArr = BytesIO()
		img.save(imgByteArr,format='PNG')
		
		apisay('Готово!',msg['toho'],photo=imgByteArr.getvalue())
