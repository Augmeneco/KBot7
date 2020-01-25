from plugins.utils import *
import subprocess, random

class main:
    level = 1
    onlyname = True
    keywords = ['дополни','продолжи','допиши']
    def execute(self,msg): 
        if msg['user_text'] == '':
            apisay('Текст то напиши',msg['toho'])
            return 0
        if msg['user_text'][-1] != ' ':
            msg['user_text'] += ' '
        for replace in ['"','\'','&',';','\\']:
            msg['user_text'] = msg['user_text'].replace(replace,'')
        curl = '''curl -s \'https://models.dobro.ai/gpt2/medium/\' -H \'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0\' -H \'Accept: */*\' -H \'Accept-Language: ru,en-US;q=0.7,en;q=0.3\' --compressed -H \'Referer: https://text.skynet.center/\' -H \'Content-Type: text/plain;charset=UTF-8\' -H \'Origin: https://text.skynet.center\' -H \'Connection: keep-alive\' --data $\'{0}\''''
        query = {"prompt":msg['user_text'],"length":30,"num_samples":1}
        curl = curl.format(json.dumps(query))

        randnum = random.randint(0,9999)
        open('/tmp/ai{0}_{1}.sh'.format(msg['userid'],randnum),'w').write(curl)

        result = json.loads(subprocess.getoutput('chmod 755 /tmp/ai{0}_{1}.sh;bash /tmp/ai{0}_{1}.sh;'.format(msg['userid'],randnum)))
        if 'replies' not in result:
            apisay('Что-то пошло не так :(',msg['toho'])
        else:
            apisay(msg['user_text']+result['replies'][0],msg['toho'])