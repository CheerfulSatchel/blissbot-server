import urllib3
from bs4 import BeautifulSoup

url = 'https://www.goodnewsnetwork.org/category/news/'

http = urllib3.PoolManager()

response = http.request('GET', url)

soup = BeautifulSoup(response.data, 'html.parser')

main_content = soup.find('div', attrs={'class': 'td-ss-main-content'})

article_block = main_content.find_all('div', attrs={'class': 'td-block-span6'})

for article in article_block:
    header = article.find('h3', attrs={'class': 'entry-title td-module-title'})
    link = header.find('a', href=True)
    print('Found link: {}'.format(link['href']))