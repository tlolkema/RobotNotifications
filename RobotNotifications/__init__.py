'''
POST a message to a Slack or Mattermost channel trough Robot Framework.

Needs at least Python 3.6 to work.

Dependency is requests.
'''
import argparse
import json

import requests
from requests.exceptions import HTTPError

__version__ = '1.0.2'
__author__ = "Tim Lolkema"


class RobotNotifications:
    '''
    POST a message to a Slack or Mattermost channel.

    Example:

    *** Settings ***
    Library   RobotNotifications   Webhook-Url

    *** Keywords ***
    Keyword
       Post Message To Channel   Message

    '''

    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, webhook):
        self.webhook = webhook

    def _clean_data(self, text, data):
        '''Validates the given arguments and creates a JSON string'''
        allowed_params = ('channel', 'username', 'icon_url', 'icon_emoji', 'props')
        json_data = {'text': text}
        for key, value in data.items():
            if key in allowed_params:
                json_data[key] = value
            else:
                raise ValueError('Invalid Parameter')
        return json.dumps(json_data)

    def post_message_to_channel(self, text, **kwargs):
        '''POST a message to a Slack or Mattermost channel.'''
        json_data = self._clean_data(text, kwargs)
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                url=self.webhook,
                data=json_data,
                headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            raise HTTPError(http_err)
        except Exception as err:
            raise Exception(err)
        else:
            print(response.text)
