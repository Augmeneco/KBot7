from plugins.utils import *
import subprocess, json

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
        
        params = json.dumps({"prompt":msg['user_text'],"length":30,"num_samples":1})
        result = requests.post('https://pelevin.gpt.dobro.ai/generate/',data=params).json()

        if 'replies' not in result:
            apisay('Что-то пошло не так :(',msg['toho'])
        else:
            apisay(msg['user_text']+result['replies'][0],msg['toho'])