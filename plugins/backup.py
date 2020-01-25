from plugins.utils import *
import sqlite3,os,time

class main:
    level = 256
    keywords = ['бк','backup']
    def execute(self,msg): 
        timer = time.time()
        if os.path.exists('/tmp/db.db'):
            os.remove('/tmp/db.db')
        db = sqlite3.connect('/tmp/db.db')
        db_cur = db.cursor()
        tables = ['system','users','dialogs']
        db_cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER,perm INTEGER,context TEXT,data TEXT)')
        db_cur.execute('CREATE TABLE IF NOT EXISTS system (name TEXT,data TEXT)')
        db_cur.execute('CREATE TABLE IF NOT EXISTS dialogs (id INTEGER,data TEXT,users TEXT)')
        for table in tables:
            msg['db_cur'].execute('SELECT * FROM '+table)
            lines = msg['db_cur'].fetchall()
            for line in lines:
                out = ''
                for row in line:
                    if type(row) == int:
                        out += str(row)+','
                    if type(row) == str:
                        out += '\''+row+'\','
                out = '('+out[:-1]+')'
                db_cur.execute('INSERT INTO '+table+' VALUES '+out)
        db.commit()

        params = {'access_token':msg['config']['group_token'],'v':'5.103','peer_id':msg['toho']}
        url = requests.post('https://api.vk.com/method/docs.getMessagesUploadServer',data=params).json()['response']['upload_url']
        with open('/tmp/db.db','rb') as f:
            ret = requests.post(url,files={'file': f}).json()['file']
        params = {'title':'db','access_token':msg['config']['group_token'],'v':'5.103','peer_id':msg['toho'],'file':ret}
        ret = requests.post('https://api.vk.com/method/docs.save',data=params).json()['response']['doc']
        
        attach = 'doc{0}_{1}'.format(ret['owner_id'],ret['id'])
        apisay(str(time.time()-timer)+' мс \nНе забудь схоронить',msg['toho'],attachment=attach)
        
        