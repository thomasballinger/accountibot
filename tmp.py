#!/usr/bin/env python
from __future__ import print_function

import zulip
import time
import threading

import credentials

# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email=credentials.email,
                      api_key=credentials.key,
                      site='recurse.zulipchat.com')

theMessage = None


class Message():
    def __init__(self, str):
        self


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

    sched = ScheduledMessages()

    def on_message(msg):
        sender_name = msg['sender_full_name']
        if sender_name == 'Accountibot':
            return

        names = [d.get('full_name') for d in msg['display_recipient']
                 if d.get('full_name') != 'Accountibot']
        message = msg['content']

        sched.schedule(time.time() + 5, names, message)

    def send_ready_messages():
        print('checking for messages to send...')
        to_send = sched.get_messages()
        for _, recips, text in to_send:
            print('sending message')

            client.send_message({
                "type": "private",
                "to": "rose@happyspork.com",
                "content": text,
            })

    def set_interval(fn, interval=1):
        while True:
            time.sleep(interval)
            fn()

    t = threading.Thread(target=set_interval,
                         args=(send_ready_messages, 2))
    t.daemon = True
    t.start()
    client.call_on_each_message(on_message)
