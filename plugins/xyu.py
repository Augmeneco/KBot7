from plugins.utils import *

class main:
	level = 1
	keywords = ['хуй']
	def execute(self, msg):
		if len(msg['user_text']) == 0:
			apisay('пошёл нахуй',msg['toho'])
			return
		a=msg['user_text'].split()
		m=[u"а", u"о", u"е", u"ё", u"э", u"у", u"ю", u"я", u"и"]
		s={
			u'я':u"хуя",
			u'а':u"хуя",
			u'о':u"хуё",
			u'ё':u"хуё",
			u'е':u"хуе",
			u'э':u"хуе",
			u'у':u"хую",
			u'ю':u"хую",
			u'и':u"хуи"
		}
		r=u""
		try:
			for n in a:
				if len(n)<4:
					r+=n+" "
				elif n[0] in m and n[2] == n[0]:
					r+=s[n[0]]+n[3::]+" "
				elif n[0] in m:
					r+=s[n[0]]+n[1::]+" "
				elif n[1] in m and n[3] == n[1]:
					r+=s[n[1]]+n[4::]+" "
				elif n[1] in m:
					r+=s[n[1]]+n[2::]+" "
				elif n[2] in m:
					r+=s[n[2]]+n[3::]+" "
				elif n[3] in m:
					r+=s[n[3]]+n[4::]+" "
				elif n[-1] in m:
					r+=s[n[-1]]+n[5::]+" "
			apisay(r,msg['toho'])
		except Exception as e:
			apisay(str(e),msg['toho'])