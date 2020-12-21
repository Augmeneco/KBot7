import random, requests, os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from plugins.utils import *

class main:
    level = 1
    keywords = ['cas','жмых','кас']
    def execute(self, msg):
        if len(msg['attachments']) == 0:
            apisay('Картинку сунуть забыл',msg['toho'])
            return 0
        if 'photo' in msg['attachments'][0]:
            ret = msg['attachments'][0]['photo']['sizes']
            num = 0
            for size in ret:
                if size['width'] > num:
                    num = size['width']
                    url = size['url']
            ret = requests.get(url).content
            img_size = Image.open(BytesIO(ret))
            size = img_size.size
            img_size.close()
            
            if len(msg['user_text'].split(' ')) == 2:
                rescale = msg['user_text'].split(' ')
                
                if not rescale[0].isdigit() and not rescale[1].isdigit():
                    apisay('Аргументы должны быть числами',msg['toho'])
                    return 0
                if int(rescale[0]) > 100 and int(rescale[1]) > 100:
                    apisay('Нельзя больше 100',msg['toho'])
                    return 0
                if int(rescale[0]) <= 0 and int(rescale[1]) <= 0:
                    apisay('Нельзя меньше 0',msg['toho'])
                    return 0
                rescale = rescale[0]+'x'+rescale[1]+'%\!'
            else:
                rescale = '50x50%\!'  
            apisay('Жмыхаю картинку... создание шок контента может занять до 20 секунд',msg['toho'])
            open('/tmp/'+str(msg['userid'])+'.jpg','wb').write(ret)
            os.system('convert /tmp/'+str(msg['userid'])+'.jpg  -liquid-rescale '+rescale+' /tmp/'+str(msg['userid'])+'_out.jpg')
            image_obj = Image.open('/tmp/'+str(msg['userid'])+'_out.jpg').convert('RGBA')
            imgByteArr = BytesIO()
            image_obj = image_obj.resize(size)

            txt = Image.new('RGBA', size, (255,255,255,0))
            draw = ImageDraw.Draw(txt)
            text = "@chaika_cbot"
            for tsize in range(100):
                font = ImageFont.truetype('data/text.ttf', tsize) 
                textwidth, textheight = draw.textsize(text, font)
                if textwidth >= size[0]/2:
                    break
            x = size[0] - textwidth
            y = size[1] - textheight

            for off in range(3):
                draw.text((x-off, y), text, font=font, fill=(0,0,0,50)) 
                draw.text((x+off, y), text, font=font, fill=(0,0,0,50))
                draw.text((x, y+off), text, font=font, fill=(0,0,0,50))
                draw.text((x, y-off), text, font=font, fill=(0,0,0,50))
                draw.text((x-off, y+off), text, font=font, fill=(0,0,0,50))
                draw.text((x+off, y+off), text, font=font, fill=(0,0,0,50))
                draw.text((x-off, y-off), text, font=font, fill=(0,0,0,50))
                draw.text((x+off, y-off), text, font=font, fill=(0,0,0,50)) 

            draw.text((x, y), text, font=font, fill=(255,255,255,50)) 
            #image_obj = Image.alpha_composite(image_obj, txt)

            image_obj.save(imgByteArr,format='PNG')
            
            apisay('Готово',msg['toho'],photo=imgByteArr.getvalue())
            os.system('rm /tmp/'+str(msg['userid'])+'_out.jpg')
            os.system('rm /tmp/'+str(msg['userid'])+'.jpg')
            image_obj.close()