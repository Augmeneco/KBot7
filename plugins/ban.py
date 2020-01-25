from plugins.utils import *
import time

class main:
    level = 256
    onlyname = True
    keywords = ['бан','разбан']
    def execute(self,msg): 
        if 'reply_message' in msg:
            message = msg['reply_message']
        else:
            if len(msg['fwd_messages']) == 0: 
                message = msg['fwd_messages'][0]

        if msg['text_split'][1] == 'бан':
            userid = message['from_id']
            if len(msg['text_split']) >= 3:
                msg['db_cur'].execute('UPDATE users SET perm=0 WHERE id='+str(userid))
                msg['userdata']['ban_start'] = time.time()
                if '.' in msg['text_split'][2]:
                    msg['userdata']['ban_time'] = float(msg['text_split'][2])*60
                else:
                    msg['userdata']['ban_time'] = int(msg['text_split'][2])*60
                msg['db_cur'].execute('UPDATE users SET data=\'{0}\' WHERE id={1}'.format(json.dumps(msg['userdata']),userid))
                msg['db'].commit()
                apisay('Юзер {0} забанен на {1} мин.'.format(userid,msg['text_split'][2]),msg['toho'])    
            else:   
                msg['db_cur'].execute('UPDATE users SET perm=0 WHERE id='+str(userid))
                msg['db'].commit()
                apisay('Юзер {0} забанен'.format(userid),msg['toho'])

        if msg['text_split'][1] == 'разбан':
            userid = message['from_id']
            msg['db_cur'].execute('UPDATE users SET perm=1 WHERE id='+str(userid))
            msg['db'].commit()
            apisay('Юзер {0} разбанен'.format(userid),msg['toho'])