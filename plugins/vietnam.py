import requests, os
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from plugins.utils import *

class main:
	level = 1
	keywords = ['вьетнам','vietnam']
	def execute(self,msg):
		if 'photo' in msg['attachments'][0]:
			ret = msg['attachments'][0]['photo']['sizes']
			num = 0
			for size in ret:
				if size['width'] > num:
					num = size['width']
					url = size['url']
			ret = requests.get(url).content
			
			if 'vietnam.png' not in os.listdir('/tmp/'):
				img = requests.get('https://raw.githubusercontent.com/Cha14ka/kb_python/master/tmp/vietnam.png').content
				open('/tmp/vietnam.png','wb').write(img)
				pic1 = Image.open(BytesIO(img))
			else:
				pic1 = Image.open('/tmp/vietnam.png')
			pic2 = Image.open(BytesIO(ret))
			pic1 = pic1.resize(pic2.size)
			pic2 = pic2.convert('RGBA')
			pic3 = Image.alpha_composite(pic2,pic1)
			imgByteArr = BytesIO()
			pic3.save(imgByteArr,format='PNG')

			apisay('Готово',msg['toho'],photo=imgByteArr.getvalue())
		else:
			apisay('Фото забыл сунуть',msg['toho'])