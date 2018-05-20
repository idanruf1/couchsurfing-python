import winsound

import api as cs_api
import hangouts


def main():
    # This file should contain your couchsurfing email and password, separated by a newline.
    with open(r'C:\temp\courchsurfing_credentials.txt', 'r') as f:
        email, password = f.readline().strip(), f.readline().strip()

    # Set the latitude and longitude to your desired location.
    api = cs_api.Api(email, password, 32.0853, 34.7818)

    unseen_hangouts = hangouts.get_unseen_connections(api, 'latest_hangouts.txt')
    # Notify about new connections
    if unseen_hangouts:
        winsound.Beep(1000, 500)
        for hangout in unseen_hangouts:
            print('found new connection with: {}'.format(hangout['topParticipants'][0]['displayName']))

    hangouts.make_new_connections(api)


if __name__ == '__main__':
    main()
