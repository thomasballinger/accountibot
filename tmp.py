#!/usr/bin/env python
from __future__ import print_function

import collections
import threading
import time

import dateparser
import zulip

import credentials

# Keyword arguments 'email' and 'api_key' are not required if you are using ~/.zuliprc
client = zulip.Client(email=credentials.email,
                      api_key=credentials.key,
                      site='recurse.zulipchat.com')


class MessageScheduler:
    """
    >>> sched = MessageScheduler()
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


Msg = collections.namedtuple('Msg', ['recipients', 'content'])


class MessageSchedule:
    def __init__(self, time, content):
        self.time = time
        self.content = content

    @staticmethod
    def from_text(text):
        """
        Turns a message into a datetime obj and the rest of the message

        >>> MessageSchedule.from_text('10 Foo')
        MessageSchedule(10, 'Foo')
        """
        timepart, content = text.split()

        return MessageSchedule(int(timepart), content)

    def __repr__(self):
        return 'MessageSchedule({!r}, {!r})'.format(self.time, self.content)


import doctest
doctest.testmod()

# Print each message the user receives
# This is a blocking call that will run forever
if __name__ == '__main__':

    sched = MessageScheduler()

    def on_message(msg):
        sender_name = msg['sender_full_name']
        if sender_name == 'Accountibot':
            return

        emails = [d.get('email') for d in msg['display_recipient']
                  if d.get('email') != 'accounti-bot@students.hackerschool.com']
        print('we are using these emails:', emails)
        message = msg['content']

        sched.schedule(time.time() + 5, emails, message)

    def send_ready_messages():
        print('checking for messages to send...')
        to_send = sched.get_messages()
        for _, recips, text in to_send:
            print('sending message')

            client.send_message({
                "type": "private",
                "to": recips,
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
