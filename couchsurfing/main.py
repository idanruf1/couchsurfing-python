import api


def is_user_desirable(user):
    return user['age'] < 33


def main():
    # This file should contain your couchsurfing email and password, seperated by a newline.
    with open(r'C:\temp\courchsurfing_credentials.txt', 'r') as f:
        email, password = f.readline().strip(), f.readline().strip()

    a = api.Api(email, password)
    # Set this to your desired location.
    a.update_location(13.7633772, 100.4718475)

    a.join_hangouts()
    hangouts = a.get_hangouts()

    for hangout in hangouts['items']:
        type = hangout['type']
        if type == 'hangout':
            # An already ongoing hangout. Don't join
            continue
        elif type == 'userRequest':
            # A request for me
            if is_user_desirable(hangout['user']):
                print('Accepted request from: {}'.format(hangout['user']['publicName']))
                a.accept_hangout(hangout['id'])

        elif type == 'userStatus':
            # An available person
            if is_user_desirable(hangout['user']):
                print('Sent request to: {}'.format(hangout['user']['publicName']))
                a.request_hangout(hangout['id'])


if __name__ == '__main__':
    main()
