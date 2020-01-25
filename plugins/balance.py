from plugins.utils import *

class main:
    level = 256
    keywords = ['баланс']
    def execute(self, msg):
        if 'balance' not in msg['userdata']:
            msg['userdata']['balance'] = 100
            msg['db_cur'].execute(
                'UPDATE users SET data=\'{0}\' WHERE id={1}'.format(json.loads(msg['userdata']),msg['userid'])
            )
            msg['db'].commit()
            apisay('Я заметила что ты первый раз обратился к своему балансу\nНачисляю тебе 100 кбкоинов',msg['toho'])

