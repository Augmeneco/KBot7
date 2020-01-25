import subprocess, traceback
from plugins.utils import *

class main:
    level = 256
    keywords = ['eval','exec']
    def execute(self, msg):
        try:
            exec(msg['user_text'].replace('»',' ').replace('—','--'))
        except:
            apisay(traceback.format_exc(),msg['toho'])