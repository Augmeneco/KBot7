from plugins.utils import *
import random

class main:
    level = 1
    keywords = ['кто']
    def execute(self,msg):
        if msg['toho'] < 2000000000:
            apisay('Что кто? Ты тут один',msg['toho'])
            return 0
        userid = random.choice(msg['dialogusers'])
        name = vk_api('users.get',token=config['user_token'],user_ids=userid)[0]
        name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])
        if random.randint(0,1) == 0:
            apisay('Есть вероятность что '+msg['user_text']+' это - '+name,msg['toho'])
        else:
            apisay('Я уверена '+msg['user_text']+' у нас '+name,msg['toho'])