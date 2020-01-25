import requests, json, os, sys, subprocess, time, datetime, threading, sqlite3

config = json.loads(open('data/config.json','r').read())
if '-dev' in sys.argv:
    config['names'] = ['кбт','тест']

def log(text,num=0):
    print(datetime.datetime.today().strftime("%H:%M:%S")+' | ['+str(num)+'] '+text)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
class money(object):
    def __init__(self,msg):
        self.msg = msg
    def balance(self):
        pass

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

def apisay(text,toho,attachment=None,keyboard=None,photo=None):
    token = config['group_token']
    params = {'v':'5.80','access_token':token,'peer_id':toho}
    if type(photo) == bytes:
        ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
        ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',photo,'image/png')}).json()
        ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.103&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).json()
        ret = ret['response'][0]
        params['attachment'] = 'photo{0}_{1}'.format(ret['owner_id'],ret['id'])
    if type(photo) == list:
        params['attachment'] = ''
        for img in photo:
            try:
                ret = requests.get('https://api.vk.com/method/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
                ret = requests.post(ret['response']['upload_url'],files={'photo':('photo.png',img,'image/png')}).json()
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
            params['attachment'] = 'photo{0}_{1}'.format(ret['owner_id'],ret['id'])
    if keyboard != None:
        params['keyboard'] = json.dumps(keyboard,ensure_ascii=False)
    if attachment != None:
        params['attachment'] = attachment
    for chunk in chunks(text,4096):
        params['message'] = chunk
        requests.post('https://api.vk.com/method/messages.send',data=params).json() 
    



def iscommand(text,plugins,msg):
    text_split = text.split(' ')
    result = {'iscommand':False,'isbotname':False}
    cmd = False

    if len(text)==0:
        return result

    if text_split[0][0] == '/' and text_split[0][1:].lower() in config['names']:
        text_split[0] = text_split[0].lower()
        result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
        result['isbotname'] = True
        cmd = text_split[1]
    if text_split[0][0] == '/':
        if text_split[0][1:].lower() not in config['names']:
            result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
            cmd = text_split[0][1:]
    if text_split[0].lower() in config['names'] and len(text_split)>1:
        text_split[0] = text_split[0].lower()
        result['isbotname'] = True
        result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
        cmd = text_split[1]
    if text_split[0].lower() not in config['names'] and text_split[0][0] != '/':
        if 'noname' in msg['dialogdata']['params'] or msg['toho'] < 2000000000: 
            result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
            cmd = text_split[0]
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

def setcontext(name,userid,db): 
    db_cur = db.cursor()
    db_cur.execute('UPDATE users SET context=\''+name+'\' WHERE id='+str(userid))
    db.commit()
    log('Обновлён контекст для пользователя '+str(userid)+' на '+name,userid)