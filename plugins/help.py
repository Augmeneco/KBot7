from plugins.utils import *

class main:
	level = 1
	keywords = ['хелп','помощь','help','начать']
	def execute(self, msg):
		if msg['text_split'][0].lower() == 'начать' and msg['toho'] >= 2000000000 : return 0
		text = '''[ ОБЫЧНЫЙ ЮЗЕР ]
&#8195;bot_name фото - ищет картинки по запросу в гугле
&#8195;bot_name вирус - выводит информацию о Covid-19 в мире
&#8195;bot_name лот - лоттерея, как аргумент принимает ставку
&#8195;bot_name топ - топ владельцев КБкоинов
&#8195;bot_name баланс - выводит ваш баланс 
&#8195;bot_name перевод - перевод кбкоинов другому юзеру
&#8195;bot_name работа - зарабатывание кбкоинов
&#8195;bot_name викторина - игра в викторину
&#8195;bot_name позови всех - зовёт всех активных пользователей беседы
&#8195;bot_name допиши - дописывает указанный текст с помощью ИИ
&#8195;bot_name настройки - настройки бота
&#8195;bot_name погода - информация о погоде (название города как аргумент)
&#8195;bot_name арт - поиск артов по тегу (на англ)
&#8195;bot_name баш - случайная цитата с баша
&#8195;bot_name цитген - создаёт цитату великих людей с пересланным сообщением
&#8195;bot_name говнокод - берёт рандомный говнокод (как аргумент может принимать название языка на английском)
&#8195;bot_name кек - отзеркаливание картинки
&#8195;bot_name вьетнам - наложение вьетнамского флешбека на картинку
&#8195;bot_name выбери - выбирает вариант из перечисленного через разделения на "или"
&#8195;bot_name жмых - сжимает изображение через CAS, так же принимает 2 числовых аргумента, например 50 50
&#8195;bot_name 34 - поиск хентая по тегу (на англ)
&#8195;bot_name кончи - кончить на картинку
&#8195;bot_name двач - рандомный тред из b, либо указанной борды
&#8195;bot_name инфа - вероятность текста
&#8195;bot_name стата - статистика бота
&#8195;bot_name музыка - поиск музыки по запросу
&#8195;bot_name видео - поиск видео по запросу
&#8195;bot_name доки - поиск документов по запросу
&#8195;bot_name когда - когда произойдет событие
&#8195;bot_name хуй - хуефицирует текст как аргумент команды
&#8195;bot_name пинг - тест пинга бота до сервера вк

Бот доступен по следующим именам: 
&#8195;bot_use_names

Беседа бота: https://vk.cc/aaDbZ8

Автор - [id354255965|Кикер] 
Исходный код бота - https://github.com/Augmeneco/KBot7'''
		names = ', '.join([name for name in msg['config']['names']])
		text = text.replace('bot_name',msg['config']['names'][0]).replace('bot_use_names',names)
		apisay(text,msg['toho'])