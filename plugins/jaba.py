from plugins.utils import *
import random, requests
class main:
	keywords = ['жаба','бенц','жанна','жабка']
	level = 1
	def execute(self,msg):
		urls = ['https://sun9-25.userapi.com/c855528/v855528146/21d6c8/9NjmR5WHD28.jpg','https://sun9-5.userapi.com/c855528/v855528146/21d6c0/NEH5T9qnrko.jpg','https://sun9-58.userapi.com/c855528/v855528146/21d6b9/FLzXYIXpZaU.jpg','https://sun9-60.userapi.com/c855528/v855528146/21d6b0/Ku1DTVQikYE.jpg','https://sun9-13.userapi.com/c855528/v855528146/21d6a9/JkONDgJaKqY.jpg','https://sun9-70.userapi.com/c855528/v855528146/21d6a1/X03Lmik_lM8.jpg','https://sun9-49.userapi.com/c855528/v855528146/21d69a/ZLfL513dMfs.jpg']
		
		apisay('держи жабу',msg['toho'],photo=requests.get(random.choice(urls)).content)
