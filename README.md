# RobotNotifications


Send notifications to Slack or Mattermost using Robot Framework.
Can be used both as library or listener.

## Installation

The recommended installation method is pip:

    pip install robotframework-notifications

Running this command installs also the latest version of Requests


## Use as listener

robot --listener "RobotNotifications;https://webhook_url;end_suite=True;end_test=True" test.robot


## Use as library

Besides the listener functionality this library allows you to post a custom message with the use of the keyword "Post Message To Channel"

To use RobotNotifications in Robot Framework, the library needs to be imported using the ``Library`` setting as any other library. The library needs the webhook url from Slack or Mattermost as an argument.

Example:
```robotframework
*** Settings ***
Library         RobotNotifications   https://hooks.slack.com/services/--your-webhook--
```
You can retrieve this webhook url in Slack or Mattermost.

Example 2:
```robotframework
*** Settings ***
Library         RobotNotifications   https://hooks.slack.com/services/--your-webhook--
...             end_suite=True   end_test=True
```

## Write a custom message

After importing the library you have access to the keyword ``Post Message To Channel``

This keyword has one mandatory argument which is the message to post to the channel, and several optional arguments.

| Argument   | Description                                                  | Required |
| ---------- | :----------------------------------------------------------- | -------- |
| text       | Markdown-formatted message to display in the post.           | YES      |
| channel    | Overrides the channel the message posts in. Use the channel’s name and not the display name. Defaults to the channel set during webhook creation. | NO       |
| username   | Overrides the username the message posts as. Defaults to the username set during webhook creation or the webhook creator’s username if the former was not set. | NO       |
| icon_url   | Overrides the profile picture the message posts with. Defaults to the URL set during webhook creation or the webhook creator’s profile picture if the former was not set. | NO       |
| icon_emoji | Overrides the profile picture and `icon_url` parameter. Defaults to none and is not set during webhook creation. | NO       |
| props      | Sets the post `props`, a JSON property bag for storing extra or meta data on the post. | NO       |

Example:
```robotframework
*** Settings ***
Library         RobotNotifications   https://hooks.slack.com/services/--your-webhook--
Suite Setup     Start Suite
Test Teardown   Message On Failure     
    
*** Keywords ***
Start Suite
    Post Message To Channel      Testing has started!    icon_emoji=robot_face    username=Robot    
    ...                          channel=robot-notifications
    
Message On Failure
    Run Keyword If Test Failed   Post Message To Channel   ${TEST_NAME}\n${TEST_MESSAGE}   
    ...                          icon_emoji=rage   username=Robot Error   channel=robot-notifications
    
*** Test Cases ***
This Test Will Pass
    Log   This Test Will Pass
    
This Test Will Fail
    Log   ${ERROR}
```    
![slack-notifications](https://user-images.githubusercontent.com/30321659/67525403-f0701680-f6b2-11e9-8e53-7ced5ff7aff6.png)
The above example shows how the ``Post Message To Channel`` can be used in Robot Framework.

You can for example use the keyword in a test teardown to post a message if the test failed containing the test name and error message.

Automatic variables

>  https://github.com/robotframework/robotframework/blob/master/doc/userguide/src/CreatingTestData/Variables.rst#automatic-variables


## Retrieve webhook

Slack

> https://slack.com/intl/en-lv/help/articles/115005265063-incoming-webhooks-for-slack

Mattermost

>  https://docs.mattermost.com/developer/webhooks-incoming.html#simple-incoming-webhook 