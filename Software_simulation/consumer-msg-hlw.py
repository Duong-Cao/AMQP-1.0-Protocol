from proton.handlers import MessagingHandler
from proton.reactor import Container

class Receive(MessagingHandler):
    def __init__(self, url):
        super(Receive, self).__init__()
        self.url = url

    def on_start(self, event):
        event.container.create_receiver(self.url)

    def on_message(self, event):
        print(f"Received message: {event.message.body}")
        event.receiver.close()
        event.connection.close()

# Command-line options (address)
opts = {'address': "localhost:5672/examples"}

try:
    Container(Receive(opts['address'])).run()
except KeyboardInterrupt:
    pass

