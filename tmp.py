#!/usr/bin/env python
from __future__ import print_function

import zulip
import sys

import credentials

# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email=credentials.email,
                      api_key=credentials.key,
                      site='recurse.zulipchat.com')
# Send a private message
client.send_message({
    "type": "private",
    "to": "rose@happyspork.com",
    "content": "I come not, friends, to steal away your hearts."
})

theMessage = None


class Message():
    def __init__(self, str):
        self

def on_message(msg):
    names = [d.get('full_name') for d in msg['display_recipient']
             if d.get('full_name') != 'Accountibot']
    message = msg['content']
    sender_name = msg['sender_full_name']

    print(message, sender_name)
    print('message sent to:', names)
    global theMessage
    theMessage = msg


# Print each message the user receives
# This is a blocking call that will run forever
client.call_on_each_message(on_message)
