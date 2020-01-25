import subprocess, json
from plugins.utils import *

class main:
    level = 1
    keywords = ['майн']
    def execute(self, msg):
        host = '193.161.193.99:12888'
        info = json.loads(subprocess.getoutput('mcstatus '+host+' json'))
        out = '''В сети: {0}
        Пинг: {1}
        Версия: {2}
        Описание: {3}
        Игроков в сети: {4}
        Игроки: {5}'''
        out = out.format(info['online'],info['ping'],info['version'],info['motd']['translate'],info['player_count'],str(info['players']))
        apisay(out,msg['toho'])