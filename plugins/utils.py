import requests, json, os, sys, subprocess, time, datetime, threading

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
    result = {}
    cmd = False

    if text_split[0][0] == '/' and text_split[0][1:] in config['names']:
        cmd = text_split[1]
    if text_split[0][0] == '/':
        if text_split[0][1:] not in config['names']:
            cmd = text_split[0][1:]
    if text_split[0] in config['names']:
        cmd = text_split[1]
    if text_split[0] not in config['names'] and text_split[0][0] != '/':
        cmd = text_split[0]

    if cmd == False: return cmd
    for plugin in plugins:
        if cmd in plugin.main.keywords:
            result['plugin'] = plugin
            result['cmd'] = cmd
            return result
    
    return False


