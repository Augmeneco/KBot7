from plugins.utils import *

class main:
    level = 1
    keywords = ['онлайн','online']

    def execute(self,msg):
        if msg['toho'] < 2000000000:
            apisay('В лс эта команда не работает',msg['toho'])
            return

        antispam = AntiSpam(msg['userid'],msg['toho'])
        info = antispam.get('online',30)
        
        if info['CanUse']:
            ret = vk_api('messages.getConversationsById',peer_ids=msg['toho'],extended=1)

            if ret['count'] == 0:
                apisay('У бота нет админки в беседе либо никого нет в сети',msg['toho'])
                return

            ret = ret['profiles']
            out = '[ ПОЛЬЗОВАТЕЛИ В СЕТИ ]\n\n'
            for user in ret:
                if 'type' not in user:
                    out += '{}) {} {} ({})\n'.format(ret.index(user)+1,user['first_name'],user['last_name'],user['id'])
            apisay(out,msg['toho'])
            antispam.set('online')
        else:
            apisay('Не флуди котек) Ты сможешь использовать эту команду через {} секунд'.format(
                int(30-(info['Timer']))
            ),msg['toho'])