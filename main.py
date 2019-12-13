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
        plugin = importlib.import_module('plugins.'+file.replace('.py','')).main()
        plugins.append(plugin)
        log('Загружен плагин {0}, \n\tПрава: {1}\n\tКоманды: {2}'.format(file.replace('.py',''),plugin.level,plugin.keywords),0)