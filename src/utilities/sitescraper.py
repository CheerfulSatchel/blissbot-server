import urllib3
from . import constants
from bs4 import BeautifulSoup

def retrieve_article_urls():
    article_urls = []
    http = urllib3.PoolManager()
    response = http.request('GET', constants.NEWS_ENDPOINT, timeout=constants.TIMEOUT_SECONDS)

    soup = BeautifulSoup(response.data, 'html.parser')
    main_content = soup.find('div', attrs={'class': 'td-ss-main-content'})
    article_block = main_content.find_all('div', attrs={'class': 'td-block-span6'})

    for article in article_block:
        # Retrieve the article link
        article_header = article.find('h3', attrs={'class': 'entry-title td-module-title'})
        article_link = article_header.find('a', href=True)['href']
        print('Found link: {}'.format(article_link))

        # Retrieve the article category
        article_div = article.find('div', attrs={'class': 'td-module-meta-info'})
        article_category = article_div.find('a').text
        print('Found category: {}'.format(article_category))
        article_url = {
            'link': article_link,
            'category': article_category
        }
        article_urls.append(article_url)
    
    return article_urls


if __name__ == '__main__':
    retrieve_article_urls()