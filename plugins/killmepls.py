import subprocess, re, os, time
from plugins.utils import *

class main:
    level = 256
    onlyname = True
    keywords = ['смэрть','kill','убейменя']
    def execute(self, msg):
        pid = subprocess.getoutput('терм ps | grep \'python\'')[:1]
        apisay('Пока мастер сенпай :(',msg['toho'])
        subprocess.getoutput('kill -9 '+str(pid))
        time.sleep(1)
        apisay('А как я выжила...',msg['toho'])
