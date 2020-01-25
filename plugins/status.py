from plugins.utils import *
import datetime, time, subprocess, re

class main:
    level = 1
    keywords = ['стат','статус','status','stat']
    def execute(self,msg):
        status = '''[ Статистика ]
        Процессор:
        &#8195;{0}&#8195;
        ОЗУ:
        &#8195;Всего: {1} МБ
        &#8195;Использовано: {2} МБ
        &#8195;Свободно: {3} МБ
        &#8195;Использовано ботом: {4} кБ
        Бот:
        &#8195;Чат: {5}
        &#8195;Время работы: {6}
        &#8195;Обращений с включения: {7}
        &#8195;Обращений за всё время: {8}
        &#8195;Права юзера: {9}'''
        
        end_time = time.monotonic()
        RAM = re.findall('\d+',subprocess.getoutput('free -m'))
        status = status.format(subprocess.getoutput('uptime'),RAM[0],RAM[1],(int(RAM[0])-int(RAM[1])),re.findall('VmRSS:\s+(\d+) kB',open('/proc/self/status','r').read())[0],\
        msg['toho'],datetime.timedelta(seconds=end_time - msg['active']['start_time']),msg['active']['bot_uses'],\
        msg['active']['bot_uses_full'],msg['userinfo'][1])

        apisay(status,msg['toho'])