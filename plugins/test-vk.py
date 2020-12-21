import requests, time
from plugins.utils import *

class main:
    level = 1
    onlyname = True
    keywords = ['пинг','ping']
    def execute(self, msg):
        out = '– users.get ping test –\n'
        min = None
        max = None
        avg = 0
        for i in range(10): 
            timer = time.time() 
            vk_api('users.get',user_ids=354255965) 
            time_ping = (time.time()-timer)*1000
            if min==None: min = time_ping
            if max==None: max = time_ping
            if min > time_ping: min = time_ping
            if max < time_ping: max = time_ping
            avg += time_ping
            out += '{0}. {1} ms\n'.format(i+1,f'{time_ping:.2f}')
            time.sleep(1) 
        avg = avg/10
        out += 'min/avg/max: {}/{}/{} ms'.format(f'{min:.2f}',f'{avg:.2f}',f'{max:.2f}')
        apisay(out,msg['toho'])