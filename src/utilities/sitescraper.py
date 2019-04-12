import urllib3
from . import constants
from bs4 import BeautifulSoup

def retrieve_articles():
    articles = []
    http = urllib3.PoolManager()
    response = http.request('GET', constants.NEWS_ENDPOINT, timeout=constants.TIMEOUT_SECONDS)

    soup = BeautifulSoup(response.data, 'html.parser')
    main_content = soup.find('div', attrs={'class': 'td-ss-main-content'})
    article_blocks = main_content.find_all('div', attrs={'class': 'td-block-span6'})

    for article_block in article_blocks:

        # Retrieve the article image URL
        article_thumb = article_block.find('div', attrs={'class': 'td-module-thumb'})
        image_url = article_thumb.find('img')['src']
        print('Found image link: {}'.format(image_url))
        title = article_thumb.find('img')['title']
        print('Found title: {}'.format(title))

        # Retrieve the story URL
        article_header = article_block.find('h3', attrs={'class': 'entry-title td-module-title'})
        story_url = article_header.find('a', href=True)['href']
        print('Found link: {}'.format(story_url))

        # Retrieve the article category
        article_div = article_block.find('div', attrs={'class': 'td-module-meta-info'})
        category = article_div.find('a').text
        print('Found category: {}'.format(category))
        article = {
            'image_url': image_url,
            'story_url': story_url,
            'category': category,
            'title': title
        }

        articles.append(article)
    
    return articles


if __name__ == '__main__':
    retrieve_article_urls()