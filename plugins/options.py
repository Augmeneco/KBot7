import traceback
from plugins.utils import *

def opt_menu(msg):
    try:
        if msg['text'].lower().replace('/','') in ['stop','exit','выход']:
            apisay('Выхожу из настроек',msg['toho'])
            setcontext('main',msg['userid'],db)
            return 0
        if msg['text'].isdigit():
            num = int(msg['text'])
            if num not in [1,2]:
                apisay('Такого пункта нет, попробуй ещё раз',msg['toho'])
                return 0
            if num == 1:
                if msg['toho'] < 2000000000:
                    apisay('Эту настройку можно использовать лишь в беседах',msg['toho'])
                    setcontext('main',msg['userid'],db)
                    return 0
                if 'noname' in msg['dialogdata']['params']:
                    msg['dialogdata']['params'].remove('noname')
                    out = 'Режим ответов без имени бота выключен'
                else:
                    msg['dialogdata']['params'].append('noname')
                    out = 'Режим ответов без имени бота включён'
                db_cur.execute('UPDATE dialogs SET data=\'{0}\' WHERE id={1}'.format(json.dumps(msg['dialogdata']),msg['toho']))
                db.commit()
                apisay(out,msg['toho'])
                setcontext('main',msg['userid'],db)
                return 0
            if num == 2:
                if 'nospeak' in msg['dialogdata']['params']:
                    msg['dialogdata']['params'].remove('nospeak')
                    out = 'Режим разговора бота включен'
                else:
                    msg['dialogdata']['params'].append('nospeak')
                    out = 'Режим разговора бота выключен'
                db_cur.execute('UPDATE dialogs SET data=\'{0}\' WHERE id={1}'.format(json.dumps(msg['dialogdata']),msg['toho']))
                db.commit()
                apisay(out,msg['toho'])
                setcontext('main',msg['userid'],db)
                return 0
        else:
            apisay('Номер пункта должен быть числом',msg['toho'])
            return 0
    except:
        log(traceback.format_exc(),msg['toho'])
        apisay('Что-то пошло не так, возвращаю тебя в основной контекст',msg['toho'])
        setcontext('main',msg['userid'],db)


class main:
    level = 1
    keywords = ['настройки','опты','параметры']
    contexts = []
    contexts.append({
        'name':'opt_menu',
        'execute':opt_menu
    })
    def execute(self, msg):
        out = """Выберите настройку бота в беседе номером пункта (для выхода пиши "выход"):

        1) Использование без имени [NONAME]
        2) Ответ бота если команда не найдена [NOSPEAK]"""

        for param in ['noname','nospeak']:
            if param in msg['dialogdata']['params']:
                if param=='noname': out = out.replace('NONAME','Включено')
                if param=='nospeak': out = out.replace('NOSPEAK','Выключено')
            else:
                if param=='noname': out = out.replace('NONAME','Выключено')
                if param=='nospeak': out = out.replace('NOSPEAK','Включено')
        apisay(out,msg['toho'])
        setcontext('opt_menu',msg['userid'],db)