from plugins.utils import *
import random

class main:
    level = 1
    keywords = ['лот','лотерея','гача']
    def execute(self,msg):
        user = User(msg['userid'])
        user.lock_n_load()
        lot = msg['user_text']
        if not lot.isdigit():
            apisay('Число должно быть числом, интеллектуал',msg['toho'])
            return 0
        else: lot = int(lot)
        if user.bank.money == 0:
            apisay('А тебе не хватает деньжат :(\nУ тебя 0 кбкоинов',msg['toho'])
            return 0
        if user.bank.money-lot < 0:
            apisay('Твоя ставка слишком высока, ты не осилишь её, у тебя всего {0} кбкоинов'.format(user.bank.money),msg['toho'])
            return 0
        if user.bank.money-lot >= 0:
            randnum = random.randint(0,100)
            if randnum in range(0,50):
                user.bank.money -= lot
                out = 'Тебе выпало число {}, ты проиграл {} кбкоинов :(\nТеперь твой баланс: {}'.format(randnum,lot,user.bank.money)
                apisay(out,msg['toho'])
            if randnum in range(50,101):
                user.bank.money += lot
                out = 'Тебе выпало число {}, ты выиграл {} кбкоинов\nТеперь твой баланс: {}'.format(randnum,lot,user.bank.money)
                apisay(out,msg['toho'])
            if user.bank.money == 0:
                out = 'У тебя кончились кбкоины :(, придется тебе идти отрабатывать их'
                apisay(out,msg['toho'])
            user.save()