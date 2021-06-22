# RobotNotifications

> **WARNING**: Make sure you have atleast robotframework-notifications version 1.2.0 when using robotframework 4+

Send notifications to Slack or Mattermost using Robot Framework.
Can be used both as library or listener.

## Installation

The recommended installation method is pip:

    pip install robotframework-notifications

Running this command installs also the latest version of Requests


## Use as listener

```robot --listener "RobotNotifications;https://webhook_url;end_test;summary" test.robot```

Listeners are taken into use from the command line with the --listener option.

- The first argument is the name of the library.
- The second argument is the webhook url.
- Based on your preferences pick the next argument(s) from the table 

Seperate the arguments with a semicolon ;

## Optional Arguments

| Argument     	| Description        	| Example                                                                                                           	|
|--------------	|--------------------	|-------------------------------------------------------------------------------------------------------------------	|
| end_suite    	| Post suite results 	| <img src="https://github.com/tlolkema/RobotNotifications/blob/master/examples_endsuite.png?raw=true" width="341"/>     |
| summary 	    | Post a report summary | <img src="https://github.com/tlolkema/RobotNotifications/blob/master/examples_summary.png?raw=true" width="341"/>  
| end_test     	| Post failing tests 	| <img src="https://github.com/tlolkema/RobotNotifications/blob/master/examples_endtest.png?raw=true" width="341"/> 	|
| end_test_all 	| Post all tests     	| <img src="https://github.com/tlolkema/RobotNotifications/blob/master/examples_endtestall.png?raw=true" width="341"/>  |

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
...             end_suite   end_test
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
      
*** Test Cases ***
Example Test
    Post Message To Channel      This is a custom message!    icon_emoji=robot_face    username=Robot    
    ...                          channel=robot-notifications
```    
The above example shows how the ``Post Message To Channel`` can be used in Robot Framework.

## Retrieve webhook

Slack

> https://slack.com/intl/en-lv/help/articles/115005265063-incoming-webhooks-for-slack

Mattermost

>  https://docs.mattermost.com/developer/webhooks-incoming.html#simple-incoming-webhook 
