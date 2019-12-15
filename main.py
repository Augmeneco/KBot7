import requests, json, os, sys, subprocess, time, datetime, threading, importlib, sqlite3, traceback
from plugins.utils import *

config = json.loads(open('data/config.json','r').read())

params = data={'access_token':config['group_token'],'v':'5.103'}
ret = requests.post('https://api.vk.com/method/groups.getById',params).json()['response'][0]
config['id'] = ret['id']
config['name'] = ret['name']

log('{0} версии {1} от Augmeneco'.format(config['name'],config['version']),0)

if not os.path.exists('data/users.db'):
    userdb = sqlite3.connect('data/users.db')
    userdb.cursor().execute('CREATE TABLE main (id INTEGER,perm INTEGER,context TEXT,data TEXT)')
else:
    userdb = sqlite3.connect('data/users.db')

plugins = []
contexts = []
for file in os.listdir('plugins'):
    if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py']:
        plugin = importlib.import_module('plugins.'+file.replace('.py',''))
        plugins.append(plugin)
        log('Загружен плагин {0}'.format(file.replace('.py','')),0)
        if hasattr(plugin.main,'contexts'):
            contexts += plugin.main.contexts
            log('Загружены контексты из '+file.replace('.py',''),0)

params = {'access_token':config['group_token'],'v':'5.103','group_id':config['id']}
lpserver = requests.post('https://api.vk.com/method/groups.getLongPollServer',data=params,timeout=100).json()['response']
ts = lpserver['ts']
active = {'bot_uses':0}
active['start_time'] = time.monotonic()
log('Инициализация бота завершена',0)

while(True):
    try:
        try:
            response = requests.post('{0}?act=a_check&key={1}&ts={2}&wait=25'.format(lpserver['server'],lpserver['key'],ts),timeout=100).json()
            ts = response['ts']
        except Exception as error: 
            if error == KeyboardInterrupt: os._exit(0)
            params = {'access_token':config['group_token'],'v':'5.103','group_id':config['id']}
            lpserver = requests.post('https://api.vk.com/method/groups.getLongPollServer',data=params,timeout=100).json()['response']
            ts = lpserver['ts']
            log('Обновление сервера лонгполла',0)
            continue

        for updates in response['updates']:
            if updates['type'] == 'message_new':
                updates = updates['object']['message']
                msg = updates
                msg['text'] = msg['text'].lower()
                msg['toho'] = updates['peer_id']
                msg['userid'] = updates['from_id']
                msg['text_split'] = msg['text'].split(' ')
                msg['config'] = config
                if msg['userid'] <= 0:
                    continue
                userinfo = userdb.cursor().execute('SELECT * FROM main WHERE id='+str(msg['userid'])).fetchone()
                if userinfo == None:
                    userdb.cursor().execute('INSERT INTO main VALUES ({0},{1},\'{2}\',\'{3}\')'.format(msg['userid'],1,'main','{}'))
                    userdb.commit()
                    userinfo = userdb.cursor().execute('SELECT * FROM main WHERE id='+str(msg['userid'])).fetchone();
                    log('Добавлен новый пользователь '+str(msg['userid']),0)
                if userinfo[1] < 1:
                    apisay('Ты в бане :(',msg['toho'])
                    continue

                cmdinfo = iscommand(msg['text'],plugins)
                if cmdinfo != False:
                    if userinfo[1] >= cmdinfo['plugin'].main.level and userinfo[2] == 'main':
                        active['bot_uses'] += 1
                        msg['active'] = active
                        msg['userdb'] = userdb
                        msg['user_text'] = cmdinfo['user_text']
                        log('Вызвана команда '+cmdinfo['cmd']+' с текстом: '+msg['text'],msg['toho'])
                        plugin = cmdinfo['plugin'].main()
                        threading.Thread(target=plugin.execute,args=(msg,)).start()
                    if userinfo[1] < cmdinfo['plugin'].main.level:
                        apisay('Тебе недостаточно прав чтобы запустить команду. \
                        Требуемый уровень прав: '+str(cmdinfo['plugin'].main.level),msg['toho'])

                if userinfo[2] != 'main':
                    for context in contexts:
                        if context['name'] == userinfo[2]:
                            threading.Thread(target=context['execute'],args=(msg,)).start()
                            setcontext('main',msg['userid'],userdb)
                            break



    except Exception as error: 
        if error == KeyboardInterrupt: os._exit(0)
        print(traceback.format_exc())