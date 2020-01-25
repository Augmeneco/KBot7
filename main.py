import requests, json, os, sys, subprocess, time, datetime, sqlite3, threading, importlib, traceback, psycopg2
from plugins.utils import *
import plugins.handler as handler

if '-dev' in sys.argv:
    devmode = True
else: devmode = False 

config = json.loads(open('data/config.json','r').read())

params = data={'access_token':config['group_token'],'v':'5.103'}
ret = requests.post('https://api.vk.com/method/groups.getById',params).json()['response'][0]
config['id'] = ret['id']
config['name'] = ret['name']

log('{0} версии {1} от Augmeneco'.format(config['name'],config['version']),0)

if devmode:
    #db = sqlite3.connect('db')
    db = psycopg2.connect(database='kbot',user='cha14ka')
    db_cur = db.cursor()
    config['names'] = ['кбт','тест']
else:
    db = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    db_cur = db.cursor()

db_cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER,perm INTEGER,context TEXT,data TEXT)')
db_cur.execute('CREATE TABLE IF NOT EXISTS system (name TEXT,data TEXT)')
db_cur.execute('CREATE TABLE IF NOT EXISTS dialogs (id INTEGER,data TEXT,users TEXT)')
db.commit()

plugins = []
contexts = []
for file in os.listdir('plugins'):
    if os.path.isfile('plugins/'+file) and '.py' in file and file not in ['utils.py','handler.py']:
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
db_cur.execute('SELECT * FROM system WHERE name=\'uses\'')
active['bot_uses_full'] = db_cur.fetchone()
if active['bot_uses_full'] == None:
    active['bot_uses_full'] = 0
    db_cur.execute('INSERT INTO system VALUES (\'uses\',\'0\')')
    db.commit()
else: active['bot_uses_full'] = int(active['bot_uses_full'][1])



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
                msg['timer'] = time.time()
                msg['text'] = msg['text']
                msg['toho'] = updates['peer_id']
                msg['userid'] = updates['from_id']
                msg['text_split'] = msg['text'].split(' ')
                msg['config'] = config
                if msg['userid'] <= 0:
                    continue

                db_cur.execute('SELECT * FROM dialogs WHERE id='+str(msg['toho']))
                dialoginfo = db_cur.fetchone()
                if dialoginfo == None:
                    db_cur.execute('INSERT INTO dialogs VALUES ({0},\'{1}\',\'{2}\')'.format(msg['toho'],'{"params":[]}','[]'))
                    db.commit()
                    db_cur.execute('SELECT * FROM dialogs WHERE id='+str(msg['toho']))
                    dialoginfo = db_cur.fetchone()
                    log('Добавлена беседа в бд '+str(msg['userid']),0)       
  
                msg['dialogdata'] = json.loads(dialoginfo[1])

                msg['dialogusers'] = json.loads(dialoginfo[2])
                if msg['userid'] not in msg['dialogusers']:
                    msg['dialogusers'].append(msg['userid'])
                    log('Пользователь {0} добавлен бд беседы {1}'.format(msg['userid'],msg['toho']))
                    db_cur.execute('UPDATE dialogs SET users=\'{0}\' WHERE id={1}'.format(json.dumps(msg['dialogusers']),msg['toho']))
                    db.commit()

                db_cur.execute('SELECT * FROM users WHERE id='+str(msg['userid']))
                userinfo = db_cur.fetchone()

                if userinfo == None:
                    db_cur.execute('INSERT INTO users VALUES ({0},{1},\'{2}\',\'{3}\')'.format(msg['userid'],1,'main','{}'))
                    db.commit()
                    db_cur.execute('SELECT * FROM users WHERE id='+str(msg['userid']))
                    userinfo = db_cur.fetchone()
                    log('Добавлен новый пользователь '+str(msg['userid']),0)
                msg['userdata'] = json.loads(userinfo[3])
                if userinfo[1] < 1:
                    if 'ban_start' in msg['userdata']:
                        if (time.time()-msg['userdata']['ban_start']) >= msg['userdata']['ban_time']:
                            del msg['userdata']['ban_start']
                            del msg['userdata']['ban_time']
                            db_cur.execute('UPDATE users SET data=\'{0}\' WHERE id={1}'.format(json.dumps(msg['userdata']),msg['userid']))
                            db_cur.execute('UPDATE users SET perm=1 WHERE id='+str(msg['userid']))
                            db.commit()
                            userinfo[1] = 1
                        else: continue
                    else: continue

                msg['db'] = db
                msg['db_cur'] = db_cur
                cmdinfo = iscommand(msg['text'],plugins,msg)
                msg['cmdinfo'] = cmdinfo

                if cmdinfo['iscommand'] != False:
                    if userinfo[1] >= cmdinfo['plugin'].main.level and userinfo[2] == 'main':
                        active['bot_uses'] += 1
                        active['bot_uses_full'] += 1
                        db_cur.execute('UPDATE system SET data=\'{0}\' WHERE name=\'uses\''.format(active['bot_uses_full']))
                        msg['active'] = active
                        msg['userinfo'] = userinfo
                        msg['user_text'] = cmdinfo['user_text']
                        log('Вызвана команда '+cmdinfo['iscommand']+' с текстом: '+msg['text'],msg['toho'])
                        plugin = cmdinfo['plugin'].main()
                        threading.Thread(target=plugin.execute,args=(msg,)).start()
                    if userinfo[1] < cmdinfo['plugin'].main.level:
                        apisay('Тебе недостаточно прав чтобы запустить команду. \
                        Требуемый уровень прав: '+str(cmdinfo['plugin'].main.level),msg['toho'])

                if userinfo[2] != 'main':
                    for context in contexts:
                        if context['name'] == userinfo[2]:
                            threading.Thread(target=context['execute'],args=(msg,)).start()
                            #setcontext('main',msg['userid'],db)
                            break
                threading.Thread(target=handler.execute,args=(updates,msg)).start()


    except Exception as error: 
        if error == KeyboardInterrupt: os._exit(0)
        print(traceback.format_exc())