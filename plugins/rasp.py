import json, time, datetime
from plugins.utils import *

class main:
    level = 1
    keywords = ['расп']
    def execute(self, msg):
        db_cur.execute('SELECT * FROM system WHERE name=\'rasp\'')
        config = db_cur.fetchone() 
        if config == None:
            config = {"day": datetime.datetime.now().strftime('%d'), "zam": [False,False,False,False,False,False], "mode": 1}
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
            mode_text = 'Числитель'
        else:
            mode_text = 'Знаменатель'     

        rasp = [
                    [
                        [
                           ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                           ['МДК 02.01 Мобильная роботехника',514],
                           ['МДК 03.02 Системы управления базами данных',404]
                        ], 
                        [
                            ['Физическая культура','С/з'],
                            ['МДК 02.01 Микропроцессорные системы',713],
                            ['МДК 03.02 Системы управления базами данных',404],
                            ['Иностранный язык','714/515']
                        ], 
                        [
                            ['БЖД',706],
                            ['МДК 02.01 Микропроцессорные системы',613]
                        ], 
                        [
                            ['МДК 02.02 Переферийные устройства',404],
                            ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                            ['МДК 02.02 Переферийные устройства',404],
                            ['МДК 02.02 Переферийные устройства',404]
                        ], 
                        [
                            ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                            ['БЖД',706],
                            ['МДК 02.01 Микропроцессорные системы',505]

                        ], 
                        [
                            [False],
                            ['БЖД',706],
                            ['МДК 02.02 Переферийные устройства',404]
                        ]
                    ], 
                    [
                        [
                           ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                           ['МДК 02.01 Мобильная роботехника',514],
                           ['МДК 03.02 Системы управления базами данных',404]
                        ], 
                        [
                            ['Физическая культура','С/з'],
                            ['МДК 02.01 Микропроцессорные системы',713],
                            ['МДК 03.02 Системы управления базами данных',404],
                            ['Иностранный язык','714/515']
                        ], 
                        [
                            ['БЖД',706],
                            ['МДК 02.01 Микропроцессорные системы',613]
                        ], 
                        [
                            ['МДК 02.02 Переферийные устройства',404],
                            ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                            ['МДК 02.01 Мобильная робототехника',616]
                        ], 
                        [
                            ['МДК 01.02 Инструментальные средства разработки аппаратно-программных средств',718],
                            ['БЖД',706],
                            ['МДК 02.01 Микропроцессорные системы',505],
                            ['МДК 02.01 Микропроцессорные системы',505]
                        ], 
                        [
                            [False],
                            ['БЖД',706],
                            ['МДК 02.02 Переферийные устройства',404]
                        ]
                    ]
                ]
        day_names_ru = ['Понедельник','Вторник','Среда','Четверг','Пятница','Суббота']

        if len(msg['user_text'])==0:
            today=int(datetime.datetime.now().strftime('%w'))-1
            if today==-1:
                apisay('Сегодня выходной :(',msg['toho'])
                return 0
        else:
            today = int(msg['user_text'].split(' ')[0])-1
        out = '[ {0} ]\n\n{1}:\n'.format(mode_text,day_names_ru[today])
        key=1
        for value in rasp[mode][today]:

            if value[0] != False:
                out += '{0}) {1} ({2})\n'.format(key,value[0],value[1])
            else:
                out += '{0}) Пары нет\n'.format(key)
            key += 1

        if config['zam'][today] != False:
            out += '\nЗаметка на этот день:\n'+config['zam'][today]
        
        apisay(out,msg['toho'])
        