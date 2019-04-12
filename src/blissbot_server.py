import random
import json
from utilities.sitescraper import retrieve_articles
from flask_api import FlaskAPI

APP = FlaskAPI(__name__)

NEWS_URLS = retrieve_articles()

@APP.route('/example/')
def example():
    return {'hello': 'world'}

@APP.route('/random-story/')
def random_story():
    print(NEWS_URLS)
    if NEWS_URLS:
        random_idx = random.randint(0, len(NEWS_URLS) - 1)
        return success_message(NEWS_URLS[random_idx])
    else:
        return failure_message()

def success_message(msg_contents):
    return json.dumps({
        'ok': True,
        'body': msg_contents
    })

def failure_message():
    # TODO: Better body error messages LOL
    return json.dumps({
        'ok': False,
        'body': 'Something went wrong!'
    })

if __name__ == '__main__':
    APP.run(debug=True, port=4390)
    