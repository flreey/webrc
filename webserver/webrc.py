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

    @classmethod
    def close_socket(cls, sockid):
        sock = cls.socks.pop(sockid, None)
        if sock:sock.close()

class IRCCommands(object):
    def send2irc(self, msg):
        self.sock = Socks.create_socket(self.session.sid)

        try:
            self.sock.sendall(msg)
        except Exception as e:
            Socks.close_socket(self.session.sid)
            print e

    def primsg(self, msg):
        self.send2irc('PRIVMSG #%s :%s\r\n' % (self.session.channel, msg))

    def recv_irc(self):
        return self.sock.recv(1024)

class CharRoom(SocketConnection, IRCCommands):
    def on_message(self, msg):
        self.primsg(msg);
        self.recv_irc()

    @event
    def login(self, nick, password, channel):
        self.send2irc('CAP LS\r\nNICK '+nick+'\r\nUSER '+nick + ' ' + nick + ' 127.0.0.1 :'+nick+'\r\n');
        self.send(self.recv_irc())
        self.send2irc('JOIN #%s\r\n' % channel)
        self.send(self.recv_irc())

        self.session.channel = channel
        return 'success'

    def on_open(self, request):
        self.session.sid = self.session.remote_ip

        #send a heartbeat to irc server
        #when auto send client heartbeat package
        heartbeat = self.session._heartbeat
        def _heartbeat():
            heartbeat()
            import time
            self.send2irc('PING LAG%s12345\r\n' % str(int(time.time())))
        self.session._heartbeat = _heartbeat

        print 'connection: %s' % self.session.sid

    def on_close(self):
        Socks.close_socket(self.session.sid)
        print 'disconnection: %s' % self.session.sid

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
