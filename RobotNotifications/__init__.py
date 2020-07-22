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
    ROBOT_LIBRARY_VERSION = '1.1.2'
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, webhook, *args):       
        self.webhook = webhook
        self.args = args
        self.ROBOT_LIBRARY_LISTENER = self

    def _clean_data(self, text, data):
        '''Validates the given arguments and creates a JSON string'''
        allowed_params = ('channel', 'username', 'icon_url', 'icon_emoji', 'props', 'attachments')
        json_data = {}
        json_data['text'] = text
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
    
    def _get_attachments(self, status, text):
        '''Return a formatted attachment list'''
        attachments = {
            "color": '#dcdcdc',
            "text": '',
            "footer": 'RobotNotifications'
        }
        if status == 'GREEN':
            attachments['color'] = '#36a64f'
        elif status == 'RED':
            attachments['color'] = '#dc143c'
        attachments['text'] = text
        attachment_list = [attachments]
        return attachment_list

    def end_suite(self, data, result):
        '''Post the suite results to Slack or Mattermost'''        
        if 'end_suite' in self.args:
            text = f'*{result.longname}*\n'
            if result.status == 'PASS':
                attachments_data = self._get_attachments('GREEN', result.full_message)
            else:
                attachments_data = self._get_attachments('RED', result.full_message)
            self.post_message_to_channel(text, attachments=attachments_data)
        
        if 'summary' in self.args:
            if not result.parent:
                text = f'*Report Summary - {result.longname}*'  
                attachment_text = (
                    f'Total Tests : {result.statistics.all.total}\n'
                    f'Total Passed : {result.statistics.all.passed}\n'
                    f'Total Failed : {result.statistics.all.failed}'
                )
                if result.statistics.all.failed == 0:
                    attachments_data = self._get_attachments('GREEN', attachment_text)
                elif result.statistics.all.failed > 0:
                    attachments_data = self._get_attachments('RED', attachment_text)
                self.post_message_to_channel(text, attachments=attachments_data)

    def end_test(self, data, result):
        '''Post individual test results to Slack or Mattermost'''
        if result.passed:
            attachment_text = (
                f'*{result.name}*\n'
                f'{result.message}'
            )
            attachments_data = self._get_attachments('GREEN', attachment_text)
        
        if not result.passed:
            attachment_text = (
                f'*{result.name}*\n'
                f'{result.message}'
            )
            attachments_data = self._get_attachments('RED', attachment_text)
        
        if 'end_test' in self.args and not result.passed:
            self.post_message_to_channel('', attachments=attachments_data)
        
        if 'end_test_all' in self.args:
            self.post_message_to_channel('', attachments=attachments_data)
