from plugins.utils import *
import requests, random

def execute(updates,msg):
    if 'action' in updates:
        if updates['action']['type'] == 'chat_invite_user':
            if updates['action']['member_id'] == -158856938:
                out = '''‍Спасибо за приглашение!
👉🏻 Пиши мне команды через / и пробел, например: / инфа Я тебя люблю
Все команды можно узнать с помощью / помощь
💬 Если ты дашь мне доступ к переписке, я стану откликаться на одно из своих имён в помощи: vk.cc/adfqEi'''
                apisay(out,msg['toho'])
            else:
                params = {'access_token':msg['config']['group_token'],'v':'5.103','user_ids':updates['action']['member_id']}
                name = requests.post('https://api.vk.com/method/users.get',data=params).json()['response'][0]
                name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])  
                apisay('Добро пожаловать в беседу, '+name+'! Чтобы узнать команды бота пиши: \n\
                '+msg['config']['names'][0]+' помощь',msg['toho'])
        if updates['action']['type'] == 'chat_kick_user':
            params = {'access_token':msg['config']['group_token'],'v':'5.103','user_ids':updates['action']['member_id']}
            name = requests.post('https://api.vk.com/method/users.get',data=params).json()['response'][0]
            name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])  
            apisay(name+' покинул беседу (ну и похуй)',msg['toho'])
    if msg['text'].split(' ')[0].lower() in ['/f','f']:
        apisay('F',msg['toho'],attachment='photo-158856938_457255856')

    if ('@all' in msg['text']) and (msg['userid'] not in [46488248,354255965,143568047]):
        apisay(' ',msg['toho'],
               photo=requests.get('https://sun9-10.userapi.com/c858432/v858432947/217f15/iWFQjlY1aJE.jpg').content
        )

    if 'nospeak' not in msg['dialogdata']['params']:
        if msg['cmdinfo']['iscommand'] == False and msg['cmdinfo']['isbotname'] == True:
            apisay('Команда не найдена :(', msg['toho'])
    for word in ['typescript','javascript']:
        if word in msg['text'].lower():
            apisay('жс гавно',msg['toho'],attachment='photo-158856938_457279263')
            break
    if msg['text'] == '/':
        apisay('Да-да?\n\
Чтобы узнать команды бота пропиши - / помощь',msg['toho'])
    if msg['text'] in ['выход','/выход','/exit','exit']:
        setcontext('main',msg['userid'],db)
        apisay('Выполнен принудительный выход из контекста юзером '+str(msg['userid']),msg['toho'])