import warnings
import mechanize
import urllib
import re
from urlparse import urlparse
from bs4 import BeautifulSoup

class EmailScraper():
	""" Email Scraper """

	def __init__(self):
		""" """
		warnings.filterwarnings('ignore') #ignore warnings
		self.browser = self.init_mechanize()
		self.url = {}

	def init_mechanize(self):
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.set_handle_refresh(False)
		browser.addheaders =[('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]		
		return browser

	def get_hrefs_from_page(self, html):
		""" Extracts all hrefs from a page and returns as list """
		urls = self.get_all_hrefs_from_soup(html)
		return self.scrub_url_list(urls)

	def get_all_hrefs_from_soup(self, html):
		urls = []
		soup = BeautifulSoup(html, 'html.parser')
		for link in soup.find_all(href=True):
			if len(link['href'])>0:
				urls.append(link['href'])
		return urls

	def scrub_url_list(self, urls):
		""" """
		formatted_urls = []
		for url in urls:
			link = self.scrub_url(url)
			if link:
				formatted_urls.append(link)
		return self.getUniqueList(formatted_urls)		


	def scrub_url(self, url):
		""" Cleans and scrubs the URL """
		baseUrl = self.url.scheme + '://' + self.url.netloc

		filePattern = re.compile('\.(css|ppt|jpg|gif|png|js|pdf|docx)$')

		url = url.strip()
		if url[0] == '/' or url[0] == '#':
			url = baseUrl + url

		if 'mailto:' in url:
			return 
		elif not url.startswith(baseUrl):
			return 
		elif filePattern.search(url):
			return
		else:
			return url

	def get_email_addreses_from_page(self, html):
		""" Extracts all email addressed from page """
		email_pattern = "(^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$|\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b)"
		email_list = []
		soup = BeautifulSoup(html, 'html.parser')

		for tag in soup.find_all(string=re.compile(email_pattern)):
			email_list.append(tag)

		return email_list

 	def getUniqueList(self, original_list):
 		""" Returns a unique list """
 		return list(set(original_list))
		
	def scrape_emails(self, seed_url):
		""" scrapes for email addresses recursively through a domain """
		self.url = urlparse(seed_url)

		visited = []
		toVisit = []
		collectedEmails = []

		toVisit.append(seed_url)

		while len(toVisit) > 0:
			url = toVisit.pop()
			visited.append(url)
			print(url)
			url = urllib.quote(url, ':/#?')
			print(url)
		
			try:
				response = self.browser.open(url)	
				html = response.read()

				toVisit = toVisit + self.get_hrefs_from_page(html)
				collectedEmails = collectedEmails + self.get_email_addreses_from_page(html)

				toVisit = [x for x in list(set(toVisit)) if x not in visited]
				print(len(toVisit))
			except (mechanize.HTTPError, mechanize.URLError) as e:
				print(e)
			
		return self.getUniqueList(collectedEmails)

if __name__ == '__main__':
	scraper = EmailScraper()
	print(scraper.scrape_emails('http://www.valleyviewsd.org/'))
