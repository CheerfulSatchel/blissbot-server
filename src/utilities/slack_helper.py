def get_entity_details(slack_bot_client, entity_id):
    entity_details = {
        'channel': '',
        'real_name': '',
        'redirect_channel': '',
        'as_user': False
    }

    # Handle user
    if entity_id[0] == 'U':
        users_info_response = slack_bot_client.api_call(
            'users.info',
            user=entity_id
        )
        if users_info_response['ok']:
            entity_details['channel'] = '@' + \
                users_info_response['user']['name']
            entity_details['real_name'] = users_info_response['user']['real_name']
            entity_details['redirect_channel'] = users_info_response['user']['id']
            entity_details['as_user'] = True
            return entity_details
        else:
            print('SEND NO USER FOUND MESSAGE')
            return None

    # Handle channel
    elif entity_id[0] == 'C':
        conversations_info_response = slack_bot_client.api_call(
            'conversations.info',
            channel=entity_id
        )
        if conversations_info_response['ok']:
            channel_id = conversations_info_response['channel']['id']
            entity_details['channel'] = channel_id
            entity_details['real_name'] = '#' + \
                conversations_info_response['channel']['name_normalized']
            entity_details['redirect_channel'] = channel_id
            return entity_details
        else:
            print('SEND NO CHANNEL FOUND MESSAGE')
            return None

    # Unknown selection made :-(
    else:
        print('Oh noooose')
        return None


def post_message(slack_bot_client, api_call_args):
    post_message_response = slack_bot_client.api_call(
        'chat.postMessage',
        **api_call_args
    )

    return post_message_response
