''' Бот для просчета заработной платы печатников работающий на типографии Flexogroup'''

import telebot

TOKEN = '943915456:AAHcQdJoIBBq0eVuvJj5pc8ugrfU-H5-sMg'
bot = telebot.TeleBot(TOKEN)

d_time={}

def zp_flex(znak):
    try:
    	znak = znak.split(' ')
    	cmyk = int(znak[0])
    	pantone = int(znak[1])
    	metr = int(znak[2])
    	w_time = 0
    	if metr < 4000:
    		r_time = metr * 60 / 2000
    	elif metr > 4000 and metr < 8000:
    		r_time = metr * 60 / 2500
    	else:
    		r_time = metr * 60 / 3000
    	w_time += cmyk * 5 + pantone * 11 + r_time
    	return w_time
    except:
        return 'Неверный ввод'
def fl_koef(d_time):
	if d_time < 270:
		koef = 0.5
	elif d_time > 270 and d_time < 350:
		koef = 0.6
	elif d_time > 350 and d_time < 410:
		koef = 0.7
	elif d_time > 410 and d_time < 460:
		koef = 0.8
	elif d_time > 460 and d_time < 510:
		koef = 0.9
	elif d_time > 510 and d_time < 590:
		koef = 1
	elif d_time > 590 and d_time < 650:
		koef = 1.1
	else:
		koef = 1.2
	return koef
@bot.message_handler(commands=['start'])
def handle_start(message):
	bot.send_message(message.chat.id, 'Привет! Введи три значения через пробел, количество СМУК, Pantone и метраж. Чтобы узнать коэффициент за день, используй команду /finish.')
	d_time[message.chat.id] = 0
@bot.message_handler(commands=['help'])
def handle_help(message):
	bot.send_message(message.chat.id, 'Для начала вычисления нажмите /start. Введи три значения через пробел, количество СМУК, Pantone и метраж. Чтобы узнать коэффициент за день, используй команду /finish.')
@bot.message_handler(commands=['finish'])
def handle_finish(message):
	bot.send_message(message.chat.id, 'коэффициент за день')	
	bot.send_message(message.chat.id, fl_koef(d_time[message.chat.id]))
	d_time[message.chat.id] = 0
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
	try:
		if message.text == 'print':
			bot.send_message(message.chat.id, d_time)
		else:
			d_time[message.chat.id]+= zp_flex(message.text)	
			bot.send_message(message.chat.id, 'время на тираж')	
			bot.send_message(message.chat.id, zp_flex(message.text))

			bot.send_message(message.chat.id, 'время за день')	
			bot.send_message(message.chat.id, d_time[message.chat.id])

			bot.send_message(message.chat.id, 'коэффициент за день')	
			bot.send_message(message.chat.id, fl_koef(d_time[message.chat.id]))
			print(d_time)
	except:
		bot.send_message(message.chat.id, 'Ошибка ввода. Воспользуйтесь командой /help')	

bot.polling(none_stop=True, interval=0)
