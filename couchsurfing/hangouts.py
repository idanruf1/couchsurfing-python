import json

import user_filter


def get_unseen_connections(api, latest_hangouts_file_path):
    new_hangouts = api.join_hangouts()['items']
    # Filter for valid connections
    new_hangouts = [hangout for hangout in new_hangouts if
                    hangout['type'] == 'hangout' and 'unreadCommentCount' in hangout]
    unseen_hangouts = []

    try:
        f = open(latest_hangouts_file_path, 'r+')
        old_hangouts = json.load(f)
        old_hangout_ids = [hangout['id'] for hangout in old_hangouts]

        for hangout in new_hangouts:
            if hangout['id'] not in old_hangout_ids:
                unseen_hangouts.append(hangout)

        f.close()
    except FileNotFoundError:
        print('Old connections file not found, creating new one!')

    # Whether there is a file or not, create a new one with the most recent connections.
    with open(latest_hangouts_file_path, 'w') as f:
        json.dump(new_hangouts, f)

    return unseen_hangouts


def make_new_connections(api):
    hangouts = api.get_hangouts()

    for hangout in hangouts['items']:
        hangout_type = hangout['type']
        if hangout_type == 'hangout':
            # An already ongoing hangout. Don't join
            continue

        elif hangout_type == 'userRequest':
            # A request for me
            if user_filter.is_user_desirable(hangout['user']):
                print('Accepted request from: {}'.format(hangout['user']['publicName']))
                api.accept_hangout(hangout['id'])

        elif hangout_type == 'userStatus':
            # An available person
            if user_filter.is_user_desirable(hangout['user']):
                print('Sent request to: {}'.format(hangout['user']['publicName']))
                api.request_hangout(hangout['id'])
