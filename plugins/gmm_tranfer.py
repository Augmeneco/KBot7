import re
from plugins.utils import *

class main:
    level = 1
    keywords = ['перевод','transfer','отправить']
    def execute(self, msg):
        splited_text = msg['user_text'].split(maxsplit=1)
        if len(splited_text) < 2:
            apisay('Слишком мало аргументов', msg['peer_id'])
            return
        if not splited_text[0].isdigit():
            apisay('Первым аргументом длжна идти сумма перевода', msg['peer_id'])
            return
        regex_match = re.match(r'(\[((club|id)(\d+)|\S+)\|(.+)\])', splited_text[1])
        if regex_match != None:
            recv_id = int(regex_match[4])
        elif splited_text[1].isdigit():
            recv_id = int(splited_text[1])
        else:
            recv_id = int(vk_api('users.get', user_ids=splited_text[1])['id'])
            if recv_id == None:
                apisay('Такого пользователя не существует во ВКонтакте', msg['peer_id'])
                return
        
        if not User(recv_id).userexists:
            apisay('Получатель ещё не зарегистрирован в боте', msg['peer_id'])
            return

        send_id = msg['userid']

        if send_id == recv_id:
            apisay('Нельзя отправлять самому себе', msg['peer_id'])
            return

        coins = int(splited_text[0])

        send = User(send_id)
        send.lock_n_load()
        recv = User(recv_id)
        recv.lock_n_load()

        if send.bank.money >= coins:  
            send.bank.money -= coins
            send.save()
            
            recv.bank.money += coins
            recv.save()

            apisay('Перевод успешно выполнен!', msg['peer_id'])
            # sender = vk_api('users.get', user_ids=send_id, name_case='gen')
            # apisay('Вам пришёл перевод на сумму {} КБк от {} {}'.format(coins, sender['first_name'], sender['last_name']), recv_id)
        else:
            apisay('У вас недостаточно средств.\
                    Ваш баланс {} КБк, а для перевода нужно ещё {} КБк.'.format(send.bank.money,
                                                                                coins - send.bank.money),
                   msg['peer_id'])
            return 0