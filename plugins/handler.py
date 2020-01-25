from plugins.utils import *
import requests, random

def execute(updates,msg):
    if 'action' in updates:
        if updates['action']['type'] == 'chat_invite_user':
            if updates['action']['member_id'] == -158856938:
                out = '''‍Спасибо за приглашение!
👉🏻 Пиши мне команды через / и пробел, например: / инфа Я тебя люблю
Помимо команд, ты можешь общаться со мной, например: / привет
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

    if 'nospeak' not in msg['dialogdata']['params']:
        if msg['cmdinfo']['iscommand'] == False and msg['cmdinfo']['isbotname'] == True:
            if 'user_text' not in msg['cmdinfo']['user_text']:
                msg['user_text'] = msg['text']
            speak = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data={'q':msg['user_text']}).json()
            if 'text' in speak: apisay(speak['text'],msg['toho'])
            else: apisay('Команда не найдена :(', msg['toho'])
    for word in ['жс','js','джс','javascript','ts']:
        if word in msg['text'].lower():
            if word in ['js','ts']:
                if random.randint(1,100) <= 10:
                    apisay('жс гавно',msg['toho'],attachment='photo-158856938_457279263')
            if word in ['javascript','typescript','джс']:
                apisay('жс гавно',msg['toho'],attachment='photo-158856938_457279263')
            break
    if msg['text'] == '/':
        apisay('Да-да?\n\
Чтобы узнать команды бота пропиши - / помощь',msg['toho'])