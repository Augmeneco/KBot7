from plugins.utils import *

class main:
    level = 1
    keywords = ['зв','звон','звонки','звонк']
    def execute(self, msg):
        out = '''2)
&#8195;11:05-11:50
&#8195;11:55-12:40
3) 
&#8195;12:50-13:35
&#8195;13:40-14:25
Обед 
&#8195;14:25-15:00
4)
&#8195;15:00-15:45
&#8195;15:50-16:35
5)
&#8195;16:45-17:30
&#8195;17:35-18:20'''
        if msg['user_text'] == 'укр':
            out = '''2)
    &#8195;10:10-11:10
    3) 
    &#8195;11:30-12:30
    Обед 
    &#8195;12:30-13:10
    4)
    &#8195;13:10-14:10
    5)
    &#8195;14:20-15:20'''
        apisay(out,msg['toho'])