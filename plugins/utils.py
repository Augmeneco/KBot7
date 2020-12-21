import requests, json, os, sys, subprocess, time, datetime, threading, sqlite3, psycopg2

config = json.loads(open('data/config.json','r').read())

if '-dev' in sys.argv:
    devmode = True
    config['names'] = ['кбт','тест']
else: devmode = False 
if 'sqlite' in sys.argv:
    sqlite_mode = True
else: sqlite_mode = False

if devmode:
    if sqlite_mode:
        db = sqlite3.connect('db',check_same_thread=False)
    else:
        db = psycopg2.connect(database='kbot')
    db_cur = db.cursor()
    config['names'] = ['кбт','тест']
else:
    db = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    db_cur = db.cursor()

def vk_api_old(method,params):
    params['access_token'] = config['group_token']
    params['v'] = '5.103'
    return requests.post('https://api.vk.com/method/'+method,data=params).json()

def vk_api(method, token=config['group_token'], **parameters):
    url = 'https://api.vk.com/method/' + method
    parameters['access_token'] = token
    if 'v' not in parameters:
        parameters['v'] = '5.103'

    # if method.split('.')[1][:3] == 'get':
    r = requests.post(url, params=parameters)

    result = r.json()

    # print(result)

    if 'error' in result:
        log('VK ERROR #{}: "{}"\nPARAMS: {}'.format(result['error']['error_code'],
                                                    result['error']['error_msg'],
                                                    result['error']['request_params']))
        return None

    return result['response']

class AntiSpam:
    def __init__(self,user_id,peer_id):
        self.user_id = user_id
        self.peer_id = peer_id
        self.user = User_v2(user_id)
        if 'spam' not in self.user.data:
            self.user.data['spam'] = {}
    def set(self,name):
        self.user.data['spam'][name] = time.time()
        self.user.save()
    def get(self,name,timer):
        if name not in self.user.data['spam']:
            return {
                'CanUse': True,
                'Timer': 0
            }
        if (time.time()-self.user.data['spam'][name] >= timer):
            return {
                'CanUse': True,
                'Timer': 0
            }
        else:
            return {
                'CanUse': False,
                'Timer': time.time()-self.user.data['spam'][name]
            }

def IsIntOpt(num,min=0,max=10,opts=None):
    if not num.isdigit():
        return False
    if opts != None:
        if num not in opts:
            return False
    if type(num) == str: num = int(num)
    if num < min:
        return False
    if num > max:
        return False
    return True

class Dialog:
    def __init__(self,peer_id):
        print('SELECT * FROM dialogs WHERE id='+str(peer_id))
        db_cur.execute('SELECT * FROM dialogs WHERE id='+str(peer_id))
        dialoginfo = db_cur.fetchone()  
        while dialoginfo == None:
            dialoginfo = db_cur.fetchone()    
        self.peer_id = peer_id
        self.data = json.loads(dialoginfo[1])
        self.users = json.loads(dialoginfo[2])
    def save(self):
        sql = 'UPDATE dialogs SET data = \'{0}\', users = \'{1}\' WHERE id = {2}'
        sql = sql.format(json.dumps(self.data),self.users,self.peer_id)
        db_cur.execute(sql) 
        db.commit()

class User_v2:
    def __init__(self,user_id):
        self.id = user_id
        db_cur.execute('SELECT * FROM users WHERE id=%s',[self.id])
        self.info = db_cur.fetchone()
        self.NewUser = False
        if self.info == None:
            db_cur.execute(
                'INSERT INTO users VALUES (%s,%s,%s,%s)',[self.id,1,'main','{}']
            )
            db.commit()
            self.data = {}
            self.level = 1
            self.context = 'main'
            self.NewUser = True
        else:
            self.data = json.loads(self.info[3])
            self.context = self.info[2]
            self.level = self.info[1]
    def reload(self):
        db_cur.execute('SELECT * FROM users WHERE id=%s',[self.id])
        self.info = db_cur.fetchone()
        self.data = json.loads(self.info[3])
        self.level = self.info[1]
    def save(self):
        db_cur.execute('UPDATE users SET data = %s WHERE id = %s',[json.dumps(self.data),self.id])
        db.commit()
    def CmdsLock(self,lock,timeout=False):
        if timeout:
            if (time.time()-self.data['cmds_lock']['time']) >= 60*5:
                del self.data['cmds_lock']['active']
                del self.data['cmds_lock']['time']
                self.save()
                return False
            return True
        if lock==None: return
        if lock:
            self.data['cmds_lock']['active'] = True
            self.data['cmds_lock']['time'] = time.time()
            self.save()
        else:
            del self.data['cmds_lock']['active']
            del self.data['cmds_lock']['time']
            self.save()

class User:
    userid: int
    perm: int
    context: str
    data = None

    bank = None

    def __init__(self,userid):
        self.userid = userid
        self.load()
        # инициализация userdata обработчиков
        self.bank = self.Bank(self)
    
    def __del__(self):
        self.close()

    def close(self):
        db.commit()
        self._cur.close()
        # self.perm = 0
        # self.context = ''
        # self.data = None

    def save(self):
        # # получение свежей userdata и блокировка записи
        # sql = 'SELECT * FROM users WHERE id = {0};'
        # sql = sql.format(self.userid)
        # self._cur.execute(sql)
        # #print(cur.fetchone())
        # new_userdata = json.loads(self._cur.fetchone()[3])

        # # совмещение изменений userdata из объекта и userdata из БД
        # print((self.userdata.items()))
        # new_userdata.update(dict(set(self.userdata.items()) - set(self._orig_userdata.items())))
        
        # обновление записи в бд
        sql = 'UPDATE users SET data = \'{0}\', perm = {1} WHERE id = {2}'
        sql = sql.format(json.dumps(self.data),self.perm,self.userid)
        self._cur.execute(sql)
        
        # разблокировка записи
        self.close()

    def lock_n_load(self):
        self._cur = db.cursor()
        self._cur.execute('SELECT * FROM users WHERE id = {} FOR UPDATE'.format(self.userid))
        tmp = self._cur.fetchone()

        if tmp == None:
            self.userexists = False
            return None
        else: 
            self.userexists = True
        self.data = json.loads(tmp[3])
        #self._orig_data = json.loads(tmp[3])
        self.perm = tmp[1]
    
    def load(self):
        self._cur = db.cursor()
        self._cur.execute('SELECT * FROM users WHERE id = {}'.format(self.userid))
        tmp = self._cur.fetchone()

        if tmp == None:
            self.userexists = False
            return None
        else: 
            self.userexists = True
        self.data = json.loads(tmp[3])
        #self._orig_data = json.loads(tmp[3])
        self.perm = tmp[1]

    class Bank:
        def __init__(self,userobj):
            self.user = userobj
            if 'money' not in self.user.data:
                self.user.data['money'] = 100
                self.user.save()
            else:
                self._money = self.user.data['money']
        
        @property
        def money(self):
            return self.user.data['money']
        @money.setter
        def money(self, coins):
            self.user.data['money'] = coins


class TUser(object):
    def __init__(self,msg):
        db_cur.execute('SELECT data FROM users WHERE id = '+str(msg['userid']))
        self.userdata = json.loads(db_cur.fetchone()[0])
        self.msg = msg
    def save(self):
        sql = 'UPDATE users SET data = \'{0}\' WHERE id = {1}'
        sql = sql.format(json.dumps(self.userdata),self.msg['userid'])
        db_cur.execute(sql)
        db.commit()
        

def log(text,num=0):
    print(datetime.datetime.today().strftime("%H:%M:%S")+' | ['+str(num)+'] '+text)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

class TBank(object):
    def __init__(self,msg):
        self.msg = msg
        self.userdata = msg['userdata']
        if 'money' not in self.userdata:
            self.money = None
        else:
            self.money = self.userdata['money']
    def save(self):
        self.userdata['money'] = self.money
        sql = 'UPDATE users SET data = \'{0}\' WHERE id = {1}'
        sql = sql.format(json.dumps(self.userdata),self.msg['userid'])
        db_cur.execute(sql)
        db.commit()
    def load(self):
        sql = 'SELECT data FROM users WHERE id = '+str(self.msg['userid'])
        db_cur.execute(sql)
        userdata = json.loads(db_cur.fetchone()[0])
        if 'money' not in self.userdata:
            self.money = None
        else:
            self.money = self.userdata['money']
        return self 

def apisay_old(text,toho,attachment=None,keyboard={"buttons":[],"one_time":True},photo=None):
    token = config['group_token']
    if photo != None:
        ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
        try:
            with open(photo, 'rb') as f:
                ret = requests.post(ret['response']['upload_url'],files={'file1': f}).json()
        except:
            ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',photo,'image/png')}).json()
        ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
        return requests.post('https://api.vk.com/method/messages.send',data={'attachment':'photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id']),'message':text,'v':'5.80','peer_id':str(toho),'access_token':str(token),'keyboard':json.dumps(keyboard)}).json()
    for chunk in chunks(text,4096):
        requests.post('https://api.vk.com/method/messages.send',data={'access_token':token,'v':'5.80','peer_id':toho,'message':chunk,'attachment':attachment,'keyboard':json.dumps(keyboard,ensure_ascii=False)}).json()    
    return True

def apisay(text,toho,attachment=None,keyboard=None,photo=None,file=None,params={}):
    token = config['group_token']
    params = {'v':'5.80','access_token':token,'peer_id':toho}
    if type(photo) == requests.models.Response:
        ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
        ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',photo.content,'image/png')}).json()
        ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.103&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
        ret = ret['response'][0]
        params['attachment'] = 'photo{0}_{1},'.format(ret['owner_id'],ret['id'])
    if type(photo) == bytes:
        ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
        ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',photo,'image/png')}).json()
        ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.103&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
        ret = ret['response'][0]
        params['attachment'] = 'photo{0}_{1},'.format(ret['owner_id'],ret['id'])
    if type(photo) == list:
        params['attachment'] = ''
        for img in photo:
            try:
                ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
                if type(img) == bytes:
                    ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',img,'image/png')}).json()
                if type(img) == requests.models.Response:
                    ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',img.content,'image/png')}).json()
                ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.103&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
                ret = ret['response'][0]
                params['attachment'] += 'photo{0}_{1},'.format(ret['owner_id'],ret['id'])
            except: pass
        params['attachment'] = params['attachment'][:-1]
    if type(photo) == str:
        with open(photo, 'rb') as f:
            ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
            ret = requests.post(ret['response']['upload_url'],files={'file1': f}).json()
            ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.103&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
            ret = ret['response'][0]
            params['attachment'] = 'photo{0}_{1},'.format(ret['owner_id'],ret['id'])

    if file != None:
        if type(file) == str:
            url = vk_api('docs.getMessagesUploadServer', peer_id=toho)['upload_url']
            with open(file,'rb') as f:
                ret = requests.post(url,files={'file': f}).json()['file']
            ret = vk_api('docs.save',{'title':file.split('/')[-1]+'.bin','peer_id':toho,'file':ret})['response']['doc']
            if 'attachment' in params:
                params['attachment'] += 'doc{0}_{1},'.format(ret['owner_id'],ret['id'])
            else:
                params['attachment'] = 'doc{0}_{1},'.format(ret['owner_id'],ret['id'])
        if type(file) == bytes:
            url = vk_api('docs.getMessagesUploadServer', peer_id=toho)['upload_url']
            ret = requests.post(url,files={'file':('file.bin',file,'multipart/form-data')}).json()['file']
            ret = vk_api('docs.save',{'title':'file.bin','peer_id':toho,'file':ret})['response']['doc']
            if 'attachment' in params:
                params['attachment'] += 'doc{0}_{1},'.format(ret['owner_id'],ret['id'])
            else:
                params['attachment'] = 'doc{0}_{1},'.format(ret['owner_id'],ret['id'])
    if keyboard != None:
        params['keyboard'] = json.dumps(keyboard,ensure_ascii=False)
    if attachment != None:
        params['attachment'] = attachment
    for chunk in chunks(text,4096):
        params['message'] = chunk
        requests.post('https://api.vk.com/method/messages.send',data=params)
    



def iscommand(text,plugins,msg):
    text_split = text.split(' ')
    result = {'iscommand':False,'isbotname':False}
    cmd = False

    if len(text)==0:
        return result
    if not devmode:
        if text_split[0][0] == '/' and text_split[0][1:].lower() in config['names']:
            text_split[0] = text_split[0].lower()
            result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
            result['isbotname'] = True
            cmd = text_split[1]
        if text_split[0][0] == '/':
            if text_split[0][1:].lower() not in config['names']:
                result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
                cmd = text_split[0][1:]
        if len(text_split) > 1:
            if text_split[0] == '/' and text_split[1].lower() in config['names']:
                text_split[1] = text_split[0].lower()
                result['isbotname'] = True
                result['user_text'] = ' '.join(text_split).split('/ '+text_split[1])[1][1:]
                cmd = text_split[2]
            if text_split[0] == '/' and text_split[1].lower() not in config['names']:
                result['isbotname'] = True
                result['user_text'] = ' '.join(text_split).split('/ '+text_split[1])[1][1:]
                cmd = text_split[1]

    if text_split[0].lower() in config['names'] and len(text_split)>1:
        text_split[0] = text_split[0].lower()
        result['isbotname'] = True
        result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
        cmd = text_split[1]
    if text_split[0].lower() not in config['names'] and text_split[0][0] != '/':
        if 'noname' in msg['dialogdata']['params'] or msg['toho'] < 2000000000: 
            result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
            cmd = text_split[0]
    if cmd == False: return result
    for plugin in plugins:
        if cmd.lower() in plugin.main.keywords:
            if hasattr(plugin.main,'onlyname'):
                if result['isbotname'] == False and plugin.main.onlyname == True\
                and cmd != False:
                    break
            result['plugin'] = plugin
            result['iscommand'] = cmd
            result['user_text'] = text.split(result['iscommand'])[1][1:]
            return result
    return result

def username(id):
    name = vk_api('users.get',user_ids=id)[0]
    name = '[id{0}|{1} {2}]'.format(name['id'],name['first_name'],name['last_name'])  
    return name

def setcontext(name,userid,db=db): 
    db_cur = db.cursor()
    db_cur.execute('UPDATE users SET context=\''+name+'\' WHERE id='+str(userid))
    db.commit()
    log('Обновлён контекст для пользователя '+str(userid)+' на '+name,userid)

def setpeercontext(name,peer_id,db=db): 
    dialog = Dialog(peer_id)
    if name == None:
        dialog.data['params'].remove('context')
        dialog.save()
        log('Удалён контекст для беседы '+str(peer_id),peer_id)
    else:
        dialog.data['context_name'] = name
        if 'context' not in dialog.data['params']:
            dialog.data['params'].append('context')
        dialog.save()
        log('Обновлён контекст для беседы '+str(peer_id)+' на '+name,peer_id)
