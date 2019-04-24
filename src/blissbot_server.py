import random
import json
import os

from database.models import Article
from database.database import Base, Database_Session
from utilities.slack_helper import get_entity_details
from flask_api import FlaskAPI
from flask import request, make_response, Response
from slackclient import SlackClient

SLACK_BOT_CLIENT = SlackClient(os.environ.get('SLACK_BOT_ACCESS_TOKEN'))

APP = FlaskAPI(__name__)


# @APP.route('/random/')
# def random_article():
#     random_article = retrieve_random_article()
#     if random_article:
#         return success_message(random_article)
#     else:
#         return failure_message()


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

    update_message_response = SLACK_BOT_CLIENT.api_call(
        'chat.update',
        **update_message_api_call_args
    )

    return make_response("", 200)


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

    Database_Session.add(new_article)
    Database_Session.commit()


def success_message(msg_contents):
    return Response(json.dumps({
        'ok': True,
        'body': msg_contents
    }), mimetype='application/json')


def failure_message():
    # TODO: Better body error messages LOL
    return Response(json.dumps({
        'ok': False,
        'body': 'Something went wrong!'
    }), mimetype='application/json')


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

    post_message_response = SLACK_BOT_CLIENT.api_call(
        'chat.postMessage',
        **post_message_api_call_args
    )

    # TODO: Handle post message response

    payload['original_message']['attachments'].append({
        'text': 'Shared with <https://{}.slack.com/messages/{}|{}>'.format(recipient_domain, entity_response['redirect_channel'], entity_response['real_name'])
    })


if __name__ == '__main__':
    APP.run(debug=True, port=4390)
