import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from plugins.utils import *

class main:
	level = 1
	keywords = ['кончи','кончил','cum']
	def execute(self, msg):
		if len(msg['attachments']) == 0:
			apisay('Фото приложи, бака',msg['toho'])
			return
			
		if 'photo' in msg['attachments'][0]:
			ret = msg['attachments'][0]['photo']['sizes']
			num = 0
			for size in ret:
				if size['width'] > num:
					num = size['width']
					url = size['url']
		else:
			apisay('Фото приложи, бака',msg['toho'])
			return

		cum = Image.open('data/cum.png')
		cum = cum.convert('RGBA')
		out = Image.new('RGBA',(660,401),color = (0,0,0))
		photo = Image.open(requests.get(url,stream=True).raw)
		photo = photo.resize((195,264),resample=Image.BILINEAR)

		#cum.paste(photo,[218,112])
		out.paste(photo,[218,112])
		#out.paste(cum)
		out = Image.alpha_composite(out,cum)

		imgByteArr = BytesIO()
		out.save(imgByteArr,format='PNG')

		apisay('Готово!',msg['toho'],photo=imgByteArr.getvalue())