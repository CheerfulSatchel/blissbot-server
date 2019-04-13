import random
import json
import os

from utilities.sitescraper import retrieve_articles
# TODO: Use class below for modularizing code
# from utilities.slack_helper import retrieve_workspace_entities
from flask_api import FlaskAPI
from flask import request, make_response, Response
from slackclient import SlackClient

SLACK_BOT_CLIENT = SlackClient(os.environ.get('SLACK_BOT_ACCESS_TOKEN'))

APP = FlaskAPI(__name__)

NEWS_URLS = retrieve_articles()

WORKSPACE_ENTITIES = SLACK_BOT_CLIENT.api_call(
    'users.list'   
)['members']

print(WORKSPACE_ENTITIES)

@APP.route('/example/')
def example():
    return {'hello': 'world'}

@APP.route('/random/')
def random_story():
    print(NEWS_URLS)
    if NEWS_URLS:
        random_idx = random.randint(0, len(NEWS_URLS) - 1)
        return success_message(NEWS_URLS[random_idx])
    else:
        return failure_message()

@APP.route('/update/message', methods=['POST'])
def update_message():

    payload = json.loads(request.data['payload'])
    print(payload)

    share_with_another_user(payload)
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

    print(update_message_response)

    return make_response("", 200)

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

def share_with_another_user(payload):
    entity_id = payload['actions'][0]['selected_options'][0]['value']
    article_url = payload['original_message']['attachments'][0]['title_link']

    real_name = ''
    user_name = '@'
    print(WORKSPACE_ENTITIES)
    for workspace_entity in WORKSPACE_ENTITIES:
        if workspace_entity['id'] == entity_id:
            real_name = workspace_entity['real_name']
            user_name = user_name + workspace_entity['name']
            break

    print('Entity: {}, Real Name: {}'.format(entity_id, real_name))
    post_message_api_call_args = {
        'channel': (user_name if entity_id[0] == 'U' else entity_id),
        'text': article_url,
        'unfurl_links': True
    }

    post_message_response = SLACK_BOT_CLIENT.api_call(
        'chat.postMessage',
        **post_message_api_call_args
    )

    payload['original_message']['attachments'].append({'text': 'Shared with {}'.format(real_name)})



if __name__ == '__main__':
    APP.run(debug=True, port=4390)
    