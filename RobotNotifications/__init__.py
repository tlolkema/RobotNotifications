'''
POST a message to a Slack or Mattermost channel trough Robot Framework.
Can be used both as a library or listener.
'''

import json

import requests
from requests.exceptions import HTTPError
from robot.api.deco import keyword


class RobotNotifications:
    '''
    POST a message to a Slack or Mattermost channel.
    '''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '1.0.4'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, webhook, end_suite=None, end_test=None):       
        self.webhook = webhook
        self.end_suite_val = end_suite
        self.end_test_val = end_test
        self.ROBOT_LIBRARY_LISTENER = self

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

    @keyword('Post Message To Channel')
    def post_message_to_channel(self, text, **kwargs):
        '''POST a custom message to a Slack or Mattermost channel.'''
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

    def end_suite(self, data, result):
        '''Post the suite results to Slack or Mattermost'''
        if self.end_suite_val:
            suite_message = f'*{result.longname}*\n{result.full_message}'
            self.post_message_to_channel(suite_message, icon_emoji='robot_face')

    def end_test(self, data, result):
        '''Post failing tests to Slack or Mattermost'''
        if self.end_test_val:
            if not result.passed:
                test_message = f'*{result.name}*\n{result.message}'
                self.post_message_to_channel(test_message, icon_emoji='rage')
