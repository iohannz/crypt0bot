from crc_parser import Parser
from secret import TOKEN
import telebot
from telebot import types
from secret import CURRENCIES
from logwriter import Logger
import datetime

bot = telebot.TeleBot(TOKEN)


buttons = ["/bitcoin", "/ethereum", "/monero",
"/litecoin", "/dogecoin", "/polkadot-new", "/binance-coin"]	

strip_btns = [i.lstrip('/') for i in buttons]


@bot.message_handler(commands = ['start', 'старт'])
def options(message):
	global buttons
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
	for btn in sorted(strip_btns):
		keyboard.add(types.KeyboardButton("/" + btn))
	bot.send_message(message.chat.id, 'Choose a currency from the suggested below	: ', reply_markup=keyboard)
	#bot.register_next_step_handler(message, show_currencies)


@bot.message_handler(commands = strip_btns)
def currency_info(message):
	try:
		logger = Logger()
		logger.listen(message)
		logger.write_user(message)
		parser = Parser(message.text[1:])
		lowest, highest = parser.find_low_high_24()
		info = parser.find_info()


		bot.send_message(message.chat.id, 
		f"""Here is report of current {info['name']} statistics 👨🏽‍💻

--------------------------------------------------------------
Current {info['name']} price is [${str(info['price'])}]

{info['name']} is {info['rate']} (last 24h) {info['chart']}

Lowest / Highest prices are [{lowest} / {highest}] 

Current {info['name']} rank is [ {info['rank']} ] {info['rank_sign']}
--------------------------------------------------------------
24h Trading Volume is ${info['trading_volume_24']} 
With a market cap of ${info['market_cap']}
--------------------------------------------------------------


More information on official CoinMarketCap website :\n{parser.url}""")
		print('Successfully send a message.\n')
	except KeyError as e:
		print(e)
# 	if message.text != None:
# 		global time_before_answer
# 		msg = bot.send_message(message.chat.id, 'Цыплёнок')
# 		time_before_answer = datetime.utcnow()
# 		bot.register_next_step_handler(msg, count_speed)

# def count_speed(message):
# 	time_after_answer = datetime.utcnow()
# 	difference = str(time_after_answer - time_before_answer)
# 	print(difference)
bot.polling()