import requests, json, os, sys, subprocess, time, datetime, threading, importlib
from plugins.utils import *

config = json.loads(open('data/config.json','r').read())

params = data={'access_token':config['group_token'],'v':'5.103'}
ret = requests.post('https://api.vk.com/method/groups.getById',params).json()['response'][0]
config['id'] = ret['id']
config['name'] = ret['name']

log('{0} версии {1} от Augmeneco'.format(config['name'],config['version']),0)

plugins = []
for file in os.listdir('plugins'):
    if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py']:
        plugin = importlib.import_module('plugins.'+file.replace('.py',''))
        plugins.append(plugin)
        log('Загружен плагин {0}, \n\tПрава: {1}\n\tКоманды: {2}'.format(file.replace('.py',''),plugin.main.level,plugin.main.keywords),0)

params = {'access_token':config['group_token'],'v':'5.103','group_id':config['id']}
lpserver = requests.post('https://api.vk.com/method/groups.getLongPollServer',data=params,timeout=100).json()['response']
ts = lpserver['ts']

while(True):
    try:
        response = requests.post('{0}?act=a_check&key={1}&ts={2}&wait=25'.format(lpserver['server'],lpserver['key'],ts)).json()
        ts = response['ts']
    except Exception as error: print(error)
    for updates in response['updates']:
        if updates['type'] == 'message_new':
            updates = updates['object']['message']
            msg = updates
            msg['toho'] = updates['peer_id']
            msg['userid'] = updates['from_id']
            
            cmdinfo = iscommand(msg['text'],plugins)
            if cmdinfo != False:
                log('Вызвана команда '+cmdinfo['cmd']+' с текстом: '+msg['text'],msg['toho'])
                plugin = cmdinfo['plugin'].main()
                plugin.execute(msg)