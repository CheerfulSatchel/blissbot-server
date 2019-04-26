import random
import json
import os

from database.models import Article
from database.database import Base, Database_Session
from database.handler import fetch_random_article
from utilities.slack_helper import get_entity_details, post_message, update_message

from flask_api import FlaskAPI
from flask import request, make_response, Response
from slackclient import SlackClient

SLACK_BOT_CLIENT = SlackClient(os.environ.get('SLACK_BOT_ACCESS_TOKEN'))

APP = FlaskAPI(__name__)


@APP.route('/random/')
def random_article():
    article = fetch_random_article()
    if article:
        payload = {
            'image_url': article.image_url,
            'title': article.title,
            'title_link': article.title_link,
            'category': article.category,
            'meta_content': article.meta_content
        }
        return success_message(body=payload, msg='Fetched a random article!!!')
    else:
        return error_message(msg='Failed to fetch random article :-(')


@APP.route('/handle-interaction/', methods=['POST'])
def handle_interaction():

    payload = json.loads(request.data['payload'])

    share_with_another_entity(payload)
    channel = payload['channel']['id']
    message_ts = payload['message_ts']
    attachments = payload['original_message']['attachments']

    update_message_api_call_args = {
        'channel': channel,
        'ts': message_ts,
        'attachments': attachments
    }

    update_message_response = udpate_message(
        SLACK_BOT_CLIENT, update_message_api_call_args)

    if update_message_response['ok']:
        return success_message(msg='Updated message in channel {}'.format(channel))
    else:
        return error_message(msg='Could not update message in channel {}'.format(channel))


@APP.route('/load/', methods=['POST'])
def load_article():
    payload = request.data

    title = payload['title']
    image_url = payload['image_url']
    title_link = payload['title_link']
    category = payload['category']
    meta_content = payload['meta_content']

    new_article = Article(title=title, image_url=image_url, title_link=title_link,
                          category=category, meta_content=meta_content)

    try:
        Database_Session.add(new_article)
        Database_Session.commit()

        return success_message(body=new_article, msg='Loaded: {}'.format(new_article))

    except:
        Database_Session.rollback()

    finally:
        Database_Session.close()

        return error_message('Could not load {}'.format(new_article))


@APP.route('/post-message/', methods=['POST'])
def post_message_call():
    print(request.data)
    post_message_api_call_args = request.data

    print('POSTING FOR: {}'.format(post_message_api_call_args))

    post_message_response = post_message(
        SLACK_BOT_CLIENT, post_message_api_call_args)

    print(post_message_response)

    if post_message_response['ok']:
        return success_message(msg='Posted message~')
    else:
        return error_message(msg='Failed to post message...')


def share_with_another_entity(payload):
    entity_id = payload['actions'][0]['selected_options'][0]['value']
    article_url = payload['original_message']['attachments'][0]['title_link']
    recipient_domain = payload['team']['domain']
    sender = payload['user']['name']

    entity_response = get_entity_details(SLACK_BOT_CLIENT, entity_id)

    post_message_api_call_args = {
        'channel': entity_response['channel'],
        'text': '{} sent :heart:\n\n{}'.format(entity_response['real_name'], article_url),
        'unfurl_links': True,
        'as_user': entity_response['as_user']
    }

    post_message_response = post_message(
        SLACK_BOT_CLIENT, post_message_api_call_args)

    # TODO: Handle post message response

    payload['original_message']['attachments'].append({
        'text': 'Shared with <https://{}.slack.com/messages/{}|{}>'.format(recipient_domain, entity_response['redirect_channel'], entity_response['real_name'])
    })


def success_message(body=None, msg=''):
    return Response(json.dumps({
        'ok': True,
        'msg': 'SUCCESS: {}'.format(msg),
        'body': body
    }), mimetype='application/json')


def error_message(body=None, msg=None):
    return Response(json.dumps({
        'ok': False,
        'msg': 'ERROR: {}'.format(msg_contents),
        'body': body
    }), mimetype='application/json')


if __name__ == '__main__':
    APP.run(debug=True, port=4390)
