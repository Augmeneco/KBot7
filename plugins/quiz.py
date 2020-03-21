from plugins.utils import *
import requests, time, re, traceback
from bs4 import BeautifulSoup as bs

def get_quiz():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': '*/*',
        'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://baza-otvetov.ru',
        'Connection': 'keep-alive',
        'Referer': 'https://baza-otvetov.ru/quiz',
        'TE': 'Trailers',
    }
    index = requests.post('https://baza-otvetov.ru/quiz/ask', headers=headers).text
    index = bs(index,'html.parser')
    answtext = index.find(class_='q_id').text
    answid = index.find(class_='q_id')['id']
    opts = [opts.text.lower() for opts in index.find_all('td')]

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0',
        'Accept': '*/*',
        'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://baza-otvetov.ru',
        'Connection': 'keep-alive',
        'Referer': 'https://baza-otvetov.ru/quiz',
    } 

    data = {
        'q_id': answid,
        'answer': opts[0]
    }
    index = requests.post('https://baza-otvetov.ru/quiz/check', headers=headers, data=data).text
    index = bs(index,'html.parser')

    out = {'opts':opts,'text':answtext,'ignore':[],'timer':time.time()}

    if 'Не верно!' in index.text:
        index = index.find_all('h3')[1].text
        out['answer'] = index.split(': ')[1]
    else:
        index = index.find_all('h3')[1].text
        out['answer'] = index.split('Правильно!')[1]
    print('Ответ: ',out['answer'])
    return out

def quiz_answs(msg):
    try:
        if msg['text'].lower() == 'выход':
            setpeercontext(None,msg['toho'])
            apisay('Вы вышли из игры',msg['toho'])
            return
        dialog = Dialog(msg['toho'])
        if time.time()-dialog.data['quiz']['timer'] >= 60:
            apisay('Время вышло, никто правильно не ответил, ответ был: '+dialog.data['quiz']['answer'],msg['toho'])
            quiz = get_quiz()
            apisay('Чтобы выйти пиши "выход"\nВопрос: \n{0}\n\nВарианты ответов:\n{1}'.format(quiz['text'],'\n'.join([str(i+1)+') '+quiz['opts'][i] for i in range(len(quiz['opts']))])),msg['toho'])
            dialog.data['quiz'] = quiz
            dialog.save()
            return 
        if msg['text'].lower() == 'ответ':
            apisay('Правильный ответ: '+dialog.data['quiz']['answer'],msg['toho'])
            quiz = get_quiz()
            apisay('Чтобы выйти пиши "выход"\nВопрос: \n{0}\n\nВарианты ответов:\n{1}'.format(quiz['text'],'\n'.join([str(i+1)+') '+quiz['opts'][i] for i in range(len(quiz['opts']))])),msg['toho'])
            dialog.data['quiz'] = quiz
            dialog.save()
            return
        if msg['userid'] in dialog.data['quiz']['ignore']: return
        if msg['text'].isdigit():
            num_text = int(msg['text'])
            if num_text > 0 and num_text <= len(dialog.data['quiz']['opts']):
                num_text -= 1
                if dialog.data['quiz']['opts'][num_text] == dialog.data['quiz']['answer'].lower():
                    apisay(username(msg['userid'])+' победил! Он получает 15 кбкоинов. Правильным ответом был: '+dialog.data['quiz']['answer'],msg['toho'])
                    user = User(msg['userid'])
                    user.bank.money += 15
                    user.save()
                    quiz = get_quiz()
                    apisay('Чтобы выйти пиши "выход"\nВопрос: \n{0}\n\nВарианты ответов:\n{1}'.format(quiz['text'],'\n'.join([str(i+1)+') '+quiz['opts'][i] for i in range(len(quiz['opts']))])),msg['toho'])
                    dialog.data['quiz'] = quiz
                    dialog.save()
                    return 
                else:
                    apisay(username(msg['userid'])+' ответил не верно, твои ответы больше не принимаются',msg['toho'])
                    dialog.data['quiz']['ignore'].append(msg['userid'])
                    dialog.save()
    except:
        print(traceback.format_exc())
        apisay('Что-то пошло не так, выключаю викторину\n'+traceback.format_exc(),msg['toho'])
        setpeercontext(None,msg['toho'])
        return
 
    if msg['text'].lower() in dialog.data['quiz']['opts']:
        if msg['text'].lower() == dialog.data['quiz']['answer'].lower():
            apisay(username(msg['userid'])+' победил! Он получает 15 кбкоинов. Правильным ответом был: '+dialog.data['quiz']['answer'],msg['toho'])
            user = User(msg['userid'])
            user.bank.money += 15
            user.save()
            quiz = get_quiz()
            apisay('Чтобы выйти пиши "выход"\nВопрос: \n{0}\n\nВарианты ответов:\n{1}'.format(quiz['text'],'\n'.join([str(i+1)+') '+quiz['opts'][i] for i in range(len(quiz['opts']))])),msg['toho'])
            dialog.data['quiz'] = quiz
            dialog.save()
            return
        else:
            apisay(username(msg['userid'])+' ответил не верно, твои ответы больше не принимаются',msg['toho'])
            dialog.data['quiz']['ignore'].append(msg['userid'])
            dialog.save()

class main:
    level = 1
    keywords = ['викторина','quiz']
    peer_contexts = []
    peer_contexts.append({
        'name':'quiz_answs',
        'execute':quiz_answs,
    })
    def execute(self,msg):
        dialog = Dialog(msg['toho'])
        if 'context' in Dialog(msg['toho']).data['params']:
            apisay('Эта беседа уже находится в контексте',msg['toho'])
            return
        quiz = get_quiz()
        dialog.data['quiz'] = quiz
        apisay('Чтобы выйти пиши "выход"\nВопрос: \n{0}\n\nВарианты ответов:\n{1}'.format(quiz['text'],'\n'.join([str(i+1)+') '+quiz['opts'][i] for i in range(len(quiz['opts']))])),msg['toho'])
        dialog.save()
        setpeercontext('quiz_answs',msg['toho'])