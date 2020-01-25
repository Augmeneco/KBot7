from plugins.utils import *

class main:
    level = 256
    keywords = ['debug','дебаг']
    def execute(self, msg):
        log('Выполнено за '+str(time.time()-msg['timer'])+' мс',0)