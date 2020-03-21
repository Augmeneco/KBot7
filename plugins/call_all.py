import requests, random, traceback, time
from plugins.utils import *

class main:
	level = 1
	keywords = ['позови']
	def execute(self, msg):
		if msg['user_text'].lower() == 'всех':
			user = User(msg['userid'])
			user.lock_n_load()
			if 'call_all_last' in user.data:
				if time.time()-user.data['call_all_last'] < 3600:
					apisay('Не флуди котек :*',msg['toho'])
					return 0

			call_all_last = time.time()
			users = ' '.join(['[id{0}|&#8195;]'.format(id) for id in msg['dialogusers']])
			user.data['call_all_last'] = call_all_last
			apisay(users,msg['toho'])
			user.save()
