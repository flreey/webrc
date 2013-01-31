# -*- coding:utf-8 -*- 

from tornado import web
from tornadio2 import SocketConnection, TornadioRouter, SocketServer, event

class Socks(object):
    socks = {}

    @classmethod
    def create_socket(cls, sockid):
        sock = cls.socks.get(sockid)
        if not sock:
            import socket
            sock = socket.socket(socket.AF_INET)
            sock.connect(('localhost', 6667))
            cls.socks[sockid] = sock
        return sock

class IRCCommands(object):
    def send_irc(self, msg):
        self.sock = Socks.create_socket(self.session.remote_ip)
        self.sock.sendall(msg)

    def primsg(self, msg):
        self.sock.sendall('PRIVMSG #%s: %s\r\n' % (self.session.channel, msg))


class CharRoom(SocketConnection, IRCCommands):

    def recv_irc(self):
        return self.sock.recv(1024)

    def on_message(self, msg):
        self.primsg(msg);
        self.recv_irc()

    @event
    def login(self, nick, password, channel):
        self.send_irc('CAP LS\r\nNICK '+nick+'\r\nUSER '+nick + ' ' + nick + ' 127.0.0.1 :'+nick+'\r\n');
        self.send(self.recv_irc())
        self.send_irc('JOIN #%s\r\n' % channel)
        self.session.channel = channel
        self.send(self.recv_irc())

        return 'success'

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
