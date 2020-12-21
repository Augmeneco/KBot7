from plugins.utils import *
from bs4 import BeautifulSoup as bs

class main:
    level = 1
    keywords = ['вирус','коронавирус','корона']
    def execute(self,msg):
        if msg['user_text'] == '':
            out = '''– COVID-2019 в мире –
    Всего заболело: {0} чел.
    Выздоровело: {1} чел.
    Умерло: {2} чел.

    Данные от worldometers.info/coronavirus
    Подробнее про вирус в РФ – стопкоронавирус.рф'''
            index = requests.get('https://www.worldometers.info/coronavirus').text
            index = bs(index,'html.parser')
            args = []
            for line in index.find_all('h1'):
                args.append(int(line.parent.find('div').find('span').text.replace(',','')))
            out = out.format(args[0],args[2],args[1])
            apisay(out,msg['toho'])
        out = '– COVID-2019 в мире –\n'
        user_text_split = msg['user_text'].split(' ')
        vdata = requests.get('https://coronavirus.zone/data.json').json()
        if user_text_split[0] == 'топ': 
            if len(user_text_split)>=2:
                if IsIntOpt(user_text_split[1],min=1,max=len(vdata)):
                    if int(user_text_split[1]) > 10:
                        user = User(msg['userid'])
                        user.lock_n_load()
                        if 'covid_last' in user.data:
                            if time.time()-user.data['covid_last'] < 3600:
                                apisay('Не флуди котек :*',msg['toho'])
                                return
                        covid_last = time.time()
                        user.data['covid_last'] = covid_last
                        user.save()
                    out += ''.join(['{}) Страна: {}\n&#8195;Заболело: {}\n&#8195;Погибло: {}\n'.format(i+1,vdata[i]['region'],vdata[i]['cases'],vdata[i]['death']) for i in range(len(vdata[:int(user_text_split[1])]))])
                    apisay(out,msg['toho'])
                    return
                else:
                    apisay('Нормально число напиши',msg['toho'])
                    return
            else:
                out += ''.join(['{}) Страна: {}\n&#8195;Заболело: {}\n&#8195;Погибло: {}\n'.format(i+1,vdata[i]['region'],vdata[i]['cases'],vdata[i]['death']) for i in range(len(vdata[:10]))])
                apisay(out,msg['toho'])
                return
        if user_text_split[0] == 'поиск':
            if len(user_text_split)==0:
                apisay('Страну напиши хоть',msg['toho'])
                return
            for region in vdata:
                if region['region'].lower() == user_text_split[1].lower():
                    apisay('Страна: {}\n&#8195;Заболело: {}\n&#8195;Погибло: {}'.format(region['region'],region['cases'],region['death']),msg['toho'])
                    return
            apisay('Ничего не найдено',msg['toho'])
