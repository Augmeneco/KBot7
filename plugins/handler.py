from plugins.utils import *
import requests

def execute(updates,msg):
    if 'action' in updates:
        if updates['action']['type'] == 'chat_invite_user':
            params = {'access_token':msg['config']['group_token'],'v':'5.103','user_ids':updates['action']['member_id']}
            name = requests.post('https://api.vk.com/method/users.get',data=params).json()['response'][0]
            name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])  
            apisay('Добро пожаловать в беседу, '+name+'! Чтобы узнать команды бота пиши: \n\
            '+msg['config']['names'][0]+' помощь',msg['toho'])
        if updates['action']['type'] == 'chat_kick_user':
            params = {'access_token':msg['config']['group_token'],'v':'5.103','user_ids':updates['action']['member_id']}
            name = requests.post('https://api.vk.com/method/users.get',data=params).json()['response'][0]
            name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])  
            apisay(name+' покинул беседу (ну и плевать)',msg['toho'])
    if msg['text'].split(' ')[0] in ['/f','f']:
        apisay('F',msg['toho'],attachment='photo-158856938_457255856')
    if msg['cmdinfo']['iscommand'] == False and msg['cmdinfo']['isbotname'] == True:
        if 'user_text' not in msg['cmdinfo']['user_text']:
            msg['user_text'] = msg['text']
        speak = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data={'q':msg['user_text']}).json()
        if 'text' in speak: apisay(speak['text'],msg['toho'])
        else: apisay('Команда не найдена :(', msg['toho'])