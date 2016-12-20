import warnings
import mechanize
import urllib
from bs4 import BeautifulSoup

browser = mechanize.Browser()


browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.addheaders =[('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]

domain_url = 'http://www.wyomingvalleysubaru.com'

warnings.filterwarnings('ignore')

def get_hrefs_from_page(html):
	""" Extracts all hrefs from a page and returns as list """
	urls = []
	formatted_urls = []
	soup = None

	try:
		soup = BeautifulSoup(html, 'html.parser')
	except:
		pass

	for link in soup.find_all(href=True):
		# print(type(link))
		# print(dir(link))
		# return
		if link['href']:
			urls.append(link['href'])

	for link in urls:
		if link[0] == '/':
			formatted_urls.append(domain_url + link.strip())
		elif link[0] == '#':
			formatted_urls.append(domain_url + '/' + link.strip())
		elif 'mailto:' in link:
			continue
		elif domain_url not in link:
			continue
		else:
			formatted_urls.append(link.strip())

	formatted_urls = list(set(formatted_urls))
	return formatted_urls

def get_email_addreses_from_page(html):
	""" Extracts all email addressed from page """
	soup = None
	try:
		soup = BeautifulSoup(html, 'html.parser')
	except:
		print("Dafuk")

	href_list = []
	for link in soup.find_all(href=True):
	    if link.get('href'):
	    	href_list.append(link.get('href'))
	    
	email_list = [x for x in href_list if 'mailto' in x]

	email_list_filtered = [x for x in email_list if x != 'mailto:'.strip()]

	return email_list_filtered


	
def scrape_emails(seed_url):
	""" scrapes for email addresses recursively through a domain """
	global domain_url
	domain_url = seed_url

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
			response = browser.open(url)	
		except:
			print("Error")

		toVisit = toVisit + get_hrefs_from_page(response)
		print(len(toVisit))
		collectedEmails = collectedEmails + get_email_addreses_from_page(url)

		toVisit = [x for x in list(set(toVisit)) if x not in visited]

	print(collectedEmails)


scrape_emails('http://www.mygym.com/scranton')
