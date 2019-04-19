import urllib3
import random
from . import constants
from bs4 import BeautifulSoup

HTTP = urllib3.PoolManager()


def get_random_page_number():
    random_page_number = random.randint(
        constants.NEWS_PAGE_START, constants.NEWS_PAGE_END)

    return random_page_number


def retrieve_random_article():

    news_url = constants.NEWS_ENDPOINT + str(get_random_page_number())

    article = {}
    response = HTTP.request('GET', news_url,
                            timeout=constants.TIMEOUT_SECONDS)

    soup = BeautifulSoup(response.data, 'html.parser')
    main_content = soup.find('div', attrs={'class': 'td-ss-main-content'})
    article_blocks = main_content.find_all(
        'div', attrs={'class': 'td-block-span6'})

    if article_blocks:
        article_block = article_blocks[random.randint(
            0, len(article_blocks)-1)]
        # Retrieve the article image URL
        article_thumb = article_block.find(
            'div', attrs={'class': 'td-module-thumb'})
        image_url = article_thumb.find('img')['src']
        print('Found image link: {}'.format(image_url))
        title = article_thumb.find('img')['title']
        print('Found title: {}'.format(title))

        # Retrieve the story URL
        article_header = article_block.find(
            'h3', attrs={'class': 'entry-title td-module-title'})
        title_link = article_header.find('a', href=True)['href']
        print('Found link: {}'.format(title_link))

        meta_content = get_article_meta_content(title_link)
        print('Found meta content: {}'.format(meta_content))

        # Retrieve the article category
        article_div = article_block.find(
            'div', attrs={'class': 'td-module-meta-info'})
        category = article_div.find('a').text
        print('Found category: {}'.format(category))
        article = {
            'image_url': image_url,
            'title_link': title_link,
            'meta_content': meta_content,
            'category': category,
            'title': title
        }

    return article


def get_article_meta_content(article_link):
    response = HTTP.request('GET', article_link,
                            timeout=constants.TIMEOUT_SECONDS)
    soup = BeautifulSoup(response.data, 'html.parser')

    meta = soup.find('meta', attrs={'name': 'description'})

    return meta['content']


if __name__ == '__main__':
    retrieve_article_urls()
