import requests as r
from bs4 import BeautifulSoup

class Parser:
	def __init__(self, currency):
		try:
			self.currency = currency.text.lstrip('/')
			self.url = f"https://coinmarketcap.com/currencies{currency}"
		except AttributeError as e:
			self.currency = currency
			self.url = f"https://coinmarketcap.com/currencies/{currency}"


	def make_urls(self, currencies):
		return [(self.url + i) for i in currencies]


	def find_current_price(self):
		try:
			api = r.get(self.url)
			soup = BeautifulSoup(api.text, "html.parser")
			current_price = soup.find('div', {'class' : 'priceValue___11gHJ'}).text
			return current_price
		except AttributeError as e:
			print(e)


	#find_low_high_24
	#Output : 'Low price', 'High price' for the last 24 hrs.
	def find_low_high_24(self):
		try:
			api = r.get(self.url)
			soup = BeautifulSoup(api.text, "html.parser")
			low = soup.find('div', {'class' : 'sc-16r8icm-0 hfoyRV nowrap___2C79N'}).text
			high = soup.find('div', {'class' : 'sc-16r8icm-0 ejXAFe nowrap___2C79N'}).text
			return (low[4:], high[5:])
		except AttributeError as e:
			print(e)


	def find_rank(self):
		try:
			api = r.get(self.url)
			soup = BeautifulSoup(api.text, "html.parser")
			rank = soup.find('div', {'class' : 'namePill___3p_Ii namePillPrimary___2-GWA'}).text
			return rank.split('#')[1]
		except AttributeError as e:
			print(e)
	

	def find_info(self):
		page = r.get(self.url).content
		
		info = (BeautifulSoup(page, "html.parser").select_one('.about___1OuKY p').getText())
		name = info.split('price')[0].split(' ')[-2]
		price = ((info.split(' $')[1].split('USD'))[0])
		trading_volume_24 = ((info.split(' $')[2].split('USD'))[0])

		rate = (((info.split(' $')[2].split('USD'))[1][2:].split('%')[0].split('is ')[1]) + '%')
		if rate.split(' ')[0] == 'up':
			rate = rate.replace('up', '🔺')
		else:
			rate = rate.replace('down', '🔻')
		
		chart = ''
		if rate[0] == '🔻': chart = '📉'
		else: chart = '📈' 

		rank = info.split("#")[1].split(',')[0]
		rank_sign = ''
		if int(rank) < 16 : rank_sign = ' 🔥'

		market_cap = info.split(' $')[-1].split('USD')[0].strip()
		


		info_dict = {'info' : info, 'name' : name, 'price' : price, 'trading_volume_24' : trading_volume_24,
					 'rate' : rate, 'rank' : rank, 'market_cap' : market_cap, 'chart' : chart, 'rank_sign' : rank_sign}
	

		return(info_dict)


	#def parse(self):
	#	urls = Parser.make_urls(self)
	#	currencies = {}
	#	for url in urls:
	#		api = r.get(url)
	#		soup = BeautifulSoup(api.text, "html.parser")
	#		try:
	#			current_price = soup.find('div', {'class' : 'priceValue___11gHJ'}).text
	#			currencies[url.split('/')[-1]] = current_price
	#			print("[{:^25}] >> [{:^16}]\n".format(url.split('/')[-1], current_price))
	#		except AttributeError as e:
	#			print(e)
	#	return currencies

if __name__ == '__main__':
	p = Parser("bitcoin")
	print(p.find_info())