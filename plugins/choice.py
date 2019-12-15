import random
from plugins.utils import *

class main:
	level = 1
	keywords = ['выбери','choice']
	def execute(self, msg):
		apisay(random.choice([a for f in msg['user_text'].split(', ') for a in msg['user_text'].split(' или ')]),msg['toho'])