import subprocess
from plugins.utils import *

class main:
    level = 256
    keywords = ['терм','term','!']
    def execute(self, msg):
        cmd = msg['user_text'].replace('—','--').split('<br>')
        with open('/tmp/cmd.sh', 'w') as cl:
            for i in range(len(cmd)):
                cl.write(cmd[i]+'\n')
        shell = subprocess.getoutput('chmod 755 /tmp/cmd.sh;bash /tmp/cmd.sh')
        apisay(shell,msg['toho'])