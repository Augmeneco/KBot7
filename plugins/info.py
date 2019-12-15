import random
from plugins.utils import *

class main:
    level = 1
    keywords = ['инфа','вероятность','info','шанс']
    def execute(self, msg):
        random.seed(sum([ord(x) for x in msg['user_text']]))
        apisay('Вероятность того, что '+msg['user_text']+' равна '+str(random.randint(0,146))+'%',msg['toho'])