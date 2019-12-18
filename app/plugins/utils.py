import requests, json, os, sys, subprocess, time, datetime, threading, sqlite3

config = json.loads(open('data/config.json','r').read())

def log(text,num=0):
    print(datetime.datetime.today().strftime("%H:%M:%S")+' | ['+str(num)+'] '+text)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def apisay(text,toho,attachment=None,keyboard={"buttons":[],"one_time":True},photo=None):
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

def iscommand(text,plugins):
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
        result['user_text'] = ' '.join(text_split).split(text_split[0])[1][1:]
        cmd = text_split[0]
    if text_split[0] == '/' and text_split[1].lower() in config['names']:
        text_split[1] = text_split[0].lower()
        result['isbotname'] = True
        result['user_text'] = ' '.join(text_split).split('/ '+text_split[1])[1][1:]
        cmd = text_split[2]
    if text_split[0] == '/' and text_split[1].lower() not in config['names']:
        result['user_text'] = ' '.join(text_split).split('/ '+text_split[1])[1][1:]
        cmd = text_split[1]
    if cmd == False: return result
    for plugin in plugins:
        if cmd.lower() in plugin.main.keywords:
            result['plugin'] = plugin
            result['iscommand'] = cmd
            result['user_text'] = text.split(result['iscommand'])[1][1:]
            return result
    
    return result

def setcontext(name,userid,userdb): 
    userdb.cursor().execute('UPDATE main SET context=\''+name+'\' WHERE id='+str(userid))
    userdb.commit()
    log('Обновлён контекст для пользователя '+str(userid)+' на '+name,0)