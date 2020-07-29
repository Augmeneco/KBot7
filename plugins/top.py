from plugins.utils import *

class main:
    level = 1
    keywords = ['топ','top']
    def execute(self,msg):
        dbcur = db.cursor()
        dbcur.execute('SELECT * FROM users WHERE data LIKE \'%money%\'')
        users = dbcur.fetchall()

        if users == []:
            apisay('Что-то пошло не так',msg['toho'])
            return

        userslist = []
        for user in users:
            userdata = json.loads(user[3])
            userslist.append({'id':user[0],'money':userdata['money']})
           
        while True:
            stop = True
            for i in list(range(len(userslist))):
                if i == len(userslist)-1: continue

                if userslist[i]['money'] > userslist[i+1]['money']:
                    user1 = userslist[i]
                    user2 = userslist[i+1]
                    userslist[i] = user2
                    userslist[i+1] = user1 
                    stop = False
            if stop: break 

        out = '[ ТОП владельцев КБкоинов ]\n'
        userslist = userslist[-10:]
        userslist.reverse()

        ids = ','.join([str(i['id']) for i in userslist])
        names = vk_api('users.get',user_ids=ids)

        for i in list(range(len(userslist))):
            out += '{}) {}: {} кбкоинов\n'.format(
                i+1,
                '[id{}|{} {}]'.format(names[i]['id'],names[i]['first_name'],names[i]['last_name']),
                userslist[i]['money']
            )

        apisay(out,msg['toho'])    