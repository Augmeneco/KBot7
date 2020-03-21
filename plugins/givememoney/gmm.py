from plugins.utils import *

class GMMUserdata:
    def __init__(self,msg):
        self.userdata = msg['userdata']
        self.msg = msg
        
    def load(self):
        sql = 'SELECT data FROM users WHERE id = '+str(self.id)
        db_cur.execute(sql)
        self.userdata = json.loads(self.msg['db_cur'].fetchone()[0])
        if 'money' not in self.userdata:
            self.money = None
        else:
            self.money = self.userdata['money']
        return self 

    def save(self):
        sql = 'UPDATE users SET data = \'{0}\' WHERE id = {1}'
        sql = sql.format(json.dumps(self.userdata),self.msg['userid'])
        self.msg['db_cur'].execute(sql)
        self.msg['db'].commit()

class GMMBank:
    def __init__(self, userid):
        self.userid = userid
        self.money = 
            
    def save(self):
        self.userdata['money'] = self.money
        sql = 'UPDATE users SET data = \'{0}\' WHERE id = {1}'
        sql = sql.format(json.dumps(self.userdata),self.msg['userid'])
        db_cur.execute(sql)
        db.commit()
    def load(self):
        sql = 'SELECT data FROM users WHERE id = '+str(self.id)
        db_cur.execute(sql)
        self.userdata = json.loads(self.msg['db_cur'].fetchone()[0])
        if 'money' not in self.userdata:
            self.money = None
        else:
            self.money = self.userdata['money']
        return self 