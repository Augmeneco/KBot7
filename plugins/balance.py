from plugins.utils import *

class main:
    level = 0
    keywords = ['баланс']
    def execute(self, msg):
        user = User(msg['userid'])
        apisay('Ваш баланс: {0} кбкоинов'.format(user.bank.money),msg['toho'])
