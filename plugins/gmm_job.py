from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import io
from plugins.utils import *

def mining(msg):
  try:
    if msg['text'].replace('/','') == 'выход':
        apisay('Вы вышли из режима работы', msg['peer_id'])
        setcontext('main', msg['userid'])
        return

    if msg['text'].replace('/','') != 'пропуск':
      if msg['userdata']['gmm_job_secret'] == msg['text'].replace('/',''):
          user = User(msg['userid'])
          user.lock_n_load()
          step = user.data['gmm_job_step']
          coins = 5*step if 5*step < 100 else 100
          user.bank.money += coins
          user.data['gmm_job_step'] += 1
          user.save()
          apisay('Отлично! Вы заработали {} КБк.'.format(coins), msg['peer_id'])

      else:
          apisay('Это неправильный ответ. Вы не получаете КБкоинов. Переходим к следующему примеру.', msg['peer_id'])

    # symbols = '1234567890'
    # captcha_secret = ''.join(random.choice(symbols) for _ in range(5))
    a = random.randint(0,99)
    b = random.randint(0,99)
    op = random.choice(('+','-'))
    captcha_text = '{}{}{}'.format(a,op,b)
    captcha_secret = str(eval(captcha_text))
    img = captcha(captcha_text)

    user = User(msg['userid'])
    user.lock_n_load()
    user.data['gmm_job_secret'] = captcha_secret
    user.save()

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_png = img_bytes.getvalue()

    apisay('Следующий пример', msg['peer_id'], photo=img_png)
  except:
    apisay('Произошла какая-то ошибка. Спасаю тебя из контекста',msg['peer_id'])
    setcontext('main',msg['userid'])

class main:
    level = 1
    keywords = ['job','работа']
    contexts = [{
		'name': 'givememoney',
		'execute': mining
    }]
    def execute(self, msg):
        # symbols = '1234567890'
        # captcha_secret = ''.join(random.choice(symbols) for _ in range(5))
        a = random.randint(0,99)
        b = random.randint(0,99)
        op = random.choice(('+','-'))
        captcha_text = '{}{}{}'.format(a,op,b)
        captcha_secret = str(eval(captcha_text))
        img = captcha(captcha_text)

        userdata = User(msg['userid'])
        userdata.lock_n_load()
        userdata.data['gmm_job_secret'] = captcha_secret
        userdata.data['gmm_job_step'] = 1
        userdata.save()

        setcontext('givememoney', msg['userid'])

        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_png = img_bytes.getvalue()

        apisay('Вы включили режим заработка. Решайте примеры на картинке и зарабатывайте КБкоины.\n\
                Чтобы выйти, напишите "выход"\n\
                Вот ваша первый пример', msg['peer_id'], photo=img_png)

# FractalCaptcha.py v 0.1
# (c) Alexandr A Alexeev 2011 | http://eax.me/

# создаем капчу, содержащую символы из строки secret
def captcha(secret, width=200, height=80,
            fontName='plugins/givememoney/2006.ttf', fontSize=54,
            blur = 0):
    mask = Image.new('RGBA', (width, height))
    font = ImageFont.truetype(fontName, fontSize)

    x_offset = -10
    draw = ImageDraw.Draw(mask)
    for i in range(len(secret)):
        x_offset += 20 + int(random.random()*20)
        y_offset = -10 + int(random.random()*30)
        draw.text((x_offset, y_offset), secret[i], font=font)

    # последний символ также должен быть повернут
    angle = -10 + int(random.random()*15)
    mask = mask.rotate(angle)

    bg = plazma(width, height)
    fg = plazma(width, height)
    result = Image.composite(bg, fg, mask)

    # blur усложнит выделение границ символов
    # альтернативный вариант - гаусово размытие:
    # http://rcjp.wordpress.com/2008/04/02/gaussian-pil-image-filter/
    if blur > 0:
      for i in range(blur):
        result = result.filter(ImageFilter.BLUR)
  
    # почему-то blur иногда не действует на границах капчи
    # использовать crop?
    return result

# генерируем "плазму" размером width x height
def plazma(width, height):
  img = Image.new('RGB', (width, height))
  pix = img.load()

  for xy in [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]:
    rgb = []
    for i in range(3):
      rgb.append(int(random.random()*256))
    pix[xy[0],xy[1]] = (rgb[0], rgb[1], rgb[2])

  plazmaRec(pix, 0, 0, width-1, height-1)
  return img

# рекурсивная составля функции plazma
def plazmaRec(pix, x1, y1, x2, y2):
    if (abs(x1 - x2) <= 1) and (abs(y1 - y2) <= 1):
        return
    
    rgb = []
    for i in range(3):
        rgb.append((pix[x1, y1][i] + pix[x1, y2][i])//2)
        rgb.append((pix[x2, y1][i] + pix[x2, y2][i])//2)
        rgb.append((pix[x1, y1][i] + pix[x2, y1][i])//2)
        rgb.append((pix[x1, y2][i] + pix[x2, y2][i])//2)
      
        tmp = (pix[x1, y1][i] + pix[x1, y2][i] +
              pix[x2, y1][i] + pix[x2, y2][i])/4
        diagonal =  ((x1-x2)**2 + (y1-y2)**2)**0.5
        while True:
          delta = int ( ((random.random() - 0.5)/100 * min(100, diagonal))*255 )
          if (tmp + delta >= 0) and (tmp + delta <= 255):
            tmp += delta
            break
        rgb.append(int(tmp))

    pix[x1, (y1 + y2)//2] = (rgb[0], rgb[5], rgb[10])
    pix[x2, (y1 + y2)//2]= (rgb[1], rgb[6], rgb[11])
    pix[(x1 + x2)//2, y1] = (rgb[2], rgb[7], rgb[12])
    pix[(x1 + x2)//2, y2] = (rgb[3], rgb[8], rgb[13])  
    pix[(x1 + x2)//2, (y1 + y2)/2] = (rgb[4], rgb[9], rgb[14])
    
    plazmaRec(pix, x1, y1, (x1+x2)/2, (y1+y2)/2)
    plazmaRec(pix, (x1+x2)/2, y1, x2, (y1+y2)/2)
    plazmaRec(pix, x1, (y1+y2)/2, (x1+x2)/2, y2)
    plazmaRec(pix, (x1+x2)/2, (y1+y2)/2, x2, y2)