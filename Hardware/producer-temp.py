from __future__ import print_function
import optparse
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

import time
import random

class Send(MessagingHandler):
    def __init__(self, url):
        super(Send, self).__init__()
        self.url = url
        self.sent = False

    def on_start(self, event):
        event.container.create_sender(self.url)

    def on_sendable(self, event):
        if not self.sent:
            temp = random.random() * 100
            message_body = temp
            msg = Message(body=message_body, properties={'temperature': 'lm35'})
            event.sender.send(msg)
            self.sent = True
            event.sender.close()

    def on_accepted(self, event):
        print("Message accepted")
        event.connection.close()

    def on_disconnected(self, event):
        print("Disconnected")

# Command-line options (address)
opts = {'address': "localhost:5672/examples"}

while 1:
	try:
		Container(Send(opts['address'])).run()
		time.sleep(10)
	except KeyboardInterrupt: pass
