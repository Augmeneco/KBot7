import random
from plugins.utils import *

class main:
    level = 1
    keywords = ['когда','when']
    def execute(self, msg):
        months = ['сентября','октября','ноября','декабря','января','февраля','марта','апреля','мая','июня','июля','августа']
        random.seed(sum([ord(x) for x in msg['user_text']]))
        randnum = random.randint(0,10)
        if randnum <= 2:
            apisay(random.choice(['Когда Путин сольётся','Когда я перестану быть говнокодом','Когда ты сдохнешь']),msg['toho'])
        else:
            apisay('Я уверена '+msg['user_text']+' '+str(random.randint(1,31))+' '+random.choice(months)+' '+str(random.randint(2019,2050)),msg['toho'])