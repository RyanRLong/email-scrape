import mechanize
from bs4 import BeautifulSoup

browser = mechanize.Browser()


browser.set_handle_robots(False)
browser.set_handle_refresh(False)
browser.addheaders =[('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')]

response = browser.open('http://www.wyomingvalleysubaru.com/dealership/staff.htm')


soup = BeautifulSoup(response.read(), 'html.parser')

urls = []
formatted_urls = []

for link in soup.find_all('a'):
	urls.append(link['href'])

for link in urls:
	if link[0] == '/':
		formatted_urls.append('http://www.wyomingvalleysubaru.com' + link.strip())
	elif link[0] == '#':
		formatted_urls.append('http://www.wyomingvalleysubaru.com/' + link.strip())
	elif 'mailto:' in link:
		continue
	elif 'http://www.wyomingvalleysubaru.com/' not in link:
		continue
	else:
		formatted_urls.append(link.strip())

formatted_urls = list(set(formatted_urls))

for url in formatted_urls:
	print(url)



# href_list = []
# for link in soup.find_all('a'):
#     href_list.append(link.get('href'))
    
# email_list = [x for x in href_list if 'mailto' in x]

# email_list_filtered = [x for x in email_list if x != 'mailto:'.strip()]

# print email_list_filtered
