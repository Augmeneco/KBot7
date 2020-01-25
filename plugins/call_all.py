import requests
from plugins.utils import *

class main:
	level = 1
	keywords = ['позови']
	def execute(self, msg):
		print(msg['user_text'])
		if msg['user_text'].lower() == 'всех':
			users = ' '.join(['[id{0}|&#8195;]'.format(id) for id in msg['dialogusers']])
			apisay(users,msg['toho'])