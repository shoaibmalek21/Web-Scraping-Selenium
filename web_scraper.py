from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request

class web_scrapper(object):
	def __init__(self, location, postal, max_price, radius):
		self.location = location
		self.postal = postal
		self.max_price = max_price
		self.radius = radius

		self.url = f'https://{location}.craigslist.org/search/sss?search_distance={radius}&postal={postal}&max_price{max_price}'
		self.driver = webdriver.Firefox()
		self.delay = 3

	def load_craigslist_url(self):
		self.driver.get(self.url)
		try:
			wait = WebDriverWait(self.driver, self.delay)
			wait.until(EC.presence_of_element_located((By.ID, 'searchform')))
			print('Page is Successfully loaded')
		except TimeoutException:
			print('Wait few seconds')

	def extract_post_data(self):
		all_post = self.driver.find_elements_by_class_name('result-row')

		titles = []
		prices = []
		dates = []

		for post in all_post:
			title = post.text.split("$")
			
			if title[0] == '':
				title = title[1]
			else:
				title = title[0]

			title = title.split('\n')
			price = title[0]
			title = title[-1]

			title = title.split(" ")
			
			month = title[0]
			day = title[1]
			title = ' '.join(title[2:])
			date = month + ' ' + day

			# print('PRICE:' + price)
			# print('TITLE:' + title)
			# print('DATE:' + date)

			titles.append(title)
			dates.append(date)
			prices.append(price)

		return titles, prices, dates

	def extract_post_urls(self):
		url_list = []
		html_page = urllib.request.urlopen(self.url)
		link_soup = BeautifulSoup(html_page, 'lxml')
		for link in link_soup.findAll('a',{'class': 'result-title hdrlnk'}):
			print(link['href'])
			url_list.append(link['href'])
		return url_list

	def quit(self):
		self.driver.close()

location = 'sfbay'	
postal = '94201'
max_price = '500'
radius = '5'

scraper = web_scrapper(location, postal, max_price, radius)
scraper.load_craigslist_url()
titles, prices, dates = scraper.extract_post_data() 
print(titles)
# scraper.extract_post_urls()
# scraper.quit()