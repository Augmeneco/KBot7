#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FractalCaptcha.py v 0.1
# (c) Alexandr A Alexeev 2011 | http://eax.me/

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import random

# создаем капчу, содержащую символы из строки secret
def captcha(secret, width=200, height=80,
    fontName='plugins/givememoney/2006.ttf', fontSize=54,
    blur = 2):
  mask = Image.new('RGBA', (width, height))
  font = ImageFont.truetype(fontName, fontSize)

  x_offset = -10
  draw = ImageDraw.Draw(mask)
  for i in range(len(secret)):
    x_offset += 20 + int(random()*20)
    y_offset = -10 + int(random()*30)
    draw.text((x_offset, y_offset), secret[i], font=font)

  # последний символ также должен быть повернут
  angle = -10 + int(random()*15)
  mask = mask.rotate(angle)

  bg = plazma(width, height)
  fg = plazma(width, height)
  result = Image.composite(bg, fg, mask)

  # blur усложнит выделение границ символов
  # альтернативный вариант - гаусово размытие:
  # http://rcjp.wordpress.com/2008/04/02/gaussian-pil-image-filter/
#   if blur > 0:
#     for i in range(blur):
#       result = result.filter(ImageFilter.BLUR)
 
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
      rgb.append(int(random()*256))
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
      delta = int ( ((random() - 0.5)/100 * min(100, diagonal))*255 )
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

if __name__ == '__main__':
  result = captcha("12345")
  result.save("result.png", "PNG")