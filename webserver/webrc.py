# -*- coding:utf-8 -*- 

from tornado import web
from tornadio2 import SocketConnection, TornadioRouter, SocketServer, event

class CharRoom(SocketConnection):
    def on_message(self, msg):
        return msg

    @event
    def news(self, msg):
        print msg
        self.emit('news', 'fuck')
        return msg

# Create tornadio router
ChatRouter = TornadioRouter(CharRoom)

# Create socket application
application = web.Application(
    ChatRouter.apply_routes([]),
    debug=True,
    socket_io_port=8001
)

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # Create and start tornadio server
    SocketServer(application)
