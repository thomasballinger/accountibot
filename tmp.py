#!/usr/bin/env python
from __future__ import print_function

import zulip
import time

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



class ScheduledMessages:
    """
    >>> sched = ScheduledMessages()
    >>> sched.schedule(10**20, ['tom'], 'in far future')
    >>> len(sched.messages)
    1
    >>> sched.schedule(1, ['tom'], 'in past')
    >>> sched.get_messages()
    [(1, ['tom'], 'in past')]
    >>> len(sched.messages)
    1

    """
    def __init__(self):
        self.messages = []

    def schedule(self, time, recipients, msg):
        self.messages.append((time, recipients, msg))

    def get_messages(self):
        candidates = self.messages
        self.messages = []
        to_send = []
        now = time.time()

        for msg in candidates:
            if msg[0] < now:
                to_send.append(msg)
            else:
                self.messages.append(msg)
        return to_send

import doctest
doctest.testmod()

# Print each message the user receives
# This is a blocking call that will run forever
if __name__ == '__main__':
    client.call_on_each_message(on_message)
