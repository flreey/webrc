# -*- coding:utf-8 -*- 

import logging
import select, threading, socket
from tornado import web
from tornadio2 import SocketConnection, TornadioRouter, SocketServer, event

class SocketsManager(object):
    socks = {}

    @classmethod
    def create_socket(cls, sockid, addr=('localhost', 6667)):
        sock = cls.socks.get(sockid)
        if not sock:
            sock = socket.socket(socket.AF_INET)
            sock.connect(addr)
            cls.socks[sockid] = sock
        return sock

    @classmethod
    def close_socket(cls, sockid):
        sock = cls.socks.pop(sockid, None)
        if sock:sock.close()

    @classmethod
    def select(cls):
        while True:
            socks = cls.socks.values()
            try:
                (rfds, wfds, efds) = select.select(socks, [], [], 1)
                for rfd in rfds:
                    data = rfd.recv(4086)
                    if data:
                        for sock in socks:
                            if rfd == sock:
                                sock.send(data)
            except socket.error as e:
                print e

class IRCCommands(object):
    def send2irc(self, msg):
        self.sock = SocketsManager.create_socket(self)

        try:
            self.sock.sendall(msg)
        except Exception as e:
            SocketsManager.close_socket(self)
            #close bidirect connection
            self.session.close()
            print e

    def primsg(self, msg):
        self.send2irc('PRIVMSG #%s :%s\r\n' % (self.session.channel, msg))
        logging.debug('PRIVMSG #%s :%s\r\n' % (self.session.channel, msg))

    def recv_irc(self, bufsize=1024):
        recv = self.sock.recv(bufsize)
        return recv

    def join(self, nick, password, channel):
        self.send2irc('CAP LS\r\nNICK '+nick+'\r\nUSER '+nick + ' ' + nick + ' 127.0.0.1 :'+nick+'\r\n');
        self.send2irc('JOIN #%s\r\n' % channel)

class CharRoom(SocketConnection, IRCCommands):
    def on_message(self, msg):
        self.primsg(msg);

    @event
    def login(self, nick, password, channel):
        self.join(nick, password, channel)
        self.session.channel = channel
        logging.debug('%s: login' % nick)
        return 'success'

    def on_open(self, request):
        #send a PING package to irc server
        #when auto send client heartbeat package
        heartbeat = self.session._heartbeat
        def _heartbeat():
            heartbeat()
            if getattr(self.session, 'channel', None):
                import time
                self.send2irc('PING LAG%s12345\r\n' % str(int(time.time())))

        self.session._heartbeat = _heartbeat
        print 'connection: %s' % self

    def on_close(self):
        SocketsManager.close_socket(self)
        print 'disconnection: %s' % self

# Create tornadio router
ChatRouter = TornadioRouter(CharRoom)

# Create socket application
application = web.Application(
    ChatRouter.apply_routes([]),
    debug=True,
    socket_io_port=8001
)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    p = threading.Thread(target=SocketsManager.select)
    p.setDaemon(True)
    p.start()

    # Create and start tornadio server
    SocketServer(application)
