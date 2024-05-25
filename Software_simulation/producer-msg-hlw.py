from __future__ import print_function
import optparse
from proton import Message
from proton.handlers import MessagingHandler
from proton.reactor import Container

class Send(MessagingHandler):
    def __init__(self, url):
        super(Send, self).__init__()
        self.url = url
        self.sent = False

    def on_start(self, event):
        event.container.create_sender(self.url)

    def on_sendable(self, event):
        if not self.sent:
            message_body = "Hello World"
            msg = Message(
                body=message_body,
                properties={'Text': 'Hi'}
            )
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

try:
    Container(Send(opts['address'])).run()
except KeyboardInterrupt:
    pass
