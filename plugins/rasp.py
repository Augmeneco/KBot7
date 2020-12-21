import json, time, datetime
from plugins.utils import *

class main:
    level = 1
    keywords = ['расп']
    def execute(self, msg):
        db_cur.execute('SELECT * FROM system WHERE name=\'rasp\'')
        config = db_cur.fetchone() 
        if config == None:
            config = {"day": datetime.datetime.now().strftime('%d'), "zam": [False,False,False,False,False,False], "mode": 0}
            db_cur.execute('INSERT INTO system VALUES (\'rasp\',\'{0}\')'.format(json.dumps(config)))
            db.commit()
        else:
            config = json.loads(config[1])

        zam_data = msg['user_text'].split(' ')
        if zam_data[0]=='р' and msg['userid'] == 354255965:
            mode = zam_data[1]
            config['mode'] = int(mode)
            db_cur.execute('UPDATE system SET data=\'{0}\' WHERE name=\'rasp\''.format(json.dumps(config)))
            db.commit()
            apisay('[LOG] Тип недели изменен на '+str(mode),msg['toho']) 
            return 0
        if zam_data[0]=='сет' and msg['userid'] == 354255965:
            day = zam_data[1]
            text = ' '.join(zam_data[2:])
            config['zam'][int(day)-1] = text
            db_cur.execute('UPDATE system SET data=\'{0}\' WHERE name=\'rasp\''.format(json.dumps(config)))
            db.commit()
            apisay('Заметка добавлена',msg['toho'])
            return 0
        if zam_data[0]=='дел' and msg['userid'] == 354255965:
            day = zam_data[1]
            config['zam'][int(day)-1] = False
            db_cur.execute('UPDATE system SET data=\'{0}\' WHERE name=\'rasp\''.format(json.dumps(config)))
            db.commit()
            apisay('Заметка удалена',msg['toho'])
            return 0
        mode = config['mode']
        date_now = datetime.datetime.now().strftime('%A|%d').split('|')
        if config['day'] != date_now[1] and date_now[0] == 'Воскресенье':
            if mode==0: 
                mode=1
            else:
                mode=0
            config['mode'] = mode
            config['day'] = date_now[1]
            db_cur.execute('UPDATE system SET data=\'{0}\' WHERE name=\'rasp\''.format(json.dumps(config)))
            db.commit()
            apisay('[LOG] Тип недели изменен на '+str(mode),msg['toho']) 

        if mode==0:
            mode_text = 'Первая подгруппа'
        else:
            mode_text = 'Вторая подгруппа'     

        rasp = [
                    [
                        [
                            [False],
                            ['МДК 04.01 АНТИВИРУСНАЯ БЕЗОПАСНОСТЬ',605],
                            ['МДК 03.01 КОМПЬЮТЕРНЫЕ СЕТИ',605],
                            ['МДК 03.01 КОНСТРУИРОВАНИЕ И КОМПАНОВКА ПК',605],
                            ['МДК 03.01 КОМПЬЮТЕРНЫЕ СЕТИ',605]
                        ], 
                        [
                            [False],
                            ['МДК 03.01 ТО И РЕМОНТ СВТ',605],
                            ['ЭКОНОМИКА ОРГАНИЗАЦИИ',605],
                            ['ИНОСТРАННЫЙ ЯЗЫК',605],
                        ], 
                        [
                            [False],
                            ['МДК 03.01 КОНСТРУИРОВАНИЕ И КОМПАНОВКА ПК',605],
                            ['МДК 04.02 ЗАЩИТА ИНФОРМАЦИИ В АВТОМАТИЗИРОВАННЫХ СИСТЕМАХ',605],
                            ['МДК 04.01 ИНЖЕНЕРНО-ТЕХНИЧЕСКАЯ ЗАЩИТА ИНФОРМАЦИИ',605],
                            ['МДК 03.01 КОМПЬЮТЕРНЫЕ СЕТИ',605]
                            
                        ], 
                        [
                            [False],
                            ['МДК 03.01 КОНСТРУИРОВАНИЕ И КОМПАНОВКА ПК',605],
                            ['ЭКОНОМИКА ОРГАНИЗАЦИИ',605],
                            ['МДК 04.02 ЗАЩИТА ИНФОРМАЦИИ В АВТОМАТИЗИРОВАННЫХ СИСТЕМАХ',605]
                        ], 
                        [
                            [False],
                            ['МДК 03.01 ТО И РЕМОНТ СВТ',605],
                            ['ФИЗИЧЕСКАЯ КУЛЬТУРА','С/з'],
                            ['МДК 04.02 ЗАЩИТА ИНФОРМАЦИИ В АВТОМАТИЗИРОВАННЫХ СИСТЕМАХ',605],
                            ['МДК 04.01 ИНЖЕНЕРНО-ТЕХНИЧЕСКАЯ ЗАЩИТА ИНФОРМАЦИИ',605]
                        ]
                    ]
                ]
        day_names_ru = ['Понедельник','Вторник','Среда','Четверг','Пятница']

        if len(msg['user_text'])==0:
            today=int(datetime.datetime.now().strftime('%w'))-1
            if today==-1:
                apisay('Сегодня выходной :(',msg['toho'])
                return 0
            if today==5:
                apisay('А мы по субботам не учимся :)',msg['toho'])
                return 0
        else:
            today = int(msg['user_text'].split(' ')[0])-1
            if today==6:
                apisay('Сегодня выходной :(',msg['toho'])
                return 0
            if today==5:
                apisay('А мы по субботам не учимся :)',msg['toho'])
                return 0
            if today < 0 or today > 6:
                apisay('А ты умён',msg['toho'])
                vk_api('messages.send',random_id=__import__('random').randint(0,999999999),message='',peer_id=msg['toho'],sticker_id='50597')
                return 0
        out = '[ {0} ]\n\n{1}:\n'.format(mode_text,day_names_ru[today])
        key=1
        for value in rasp[0][today]:

            if value[0] != False:
                out += '{0}) {1} ({2})\n'.format(key,value[0],value[1])
            else:
                out += '{0}) Пары нет\n'.format(key)
            key += 1

        if config['zam'][today] != False:
            out += '\nЗаметка на этот день:\n'+config['zam'][today]
        
        apisay(out,msg['toho'])
        
