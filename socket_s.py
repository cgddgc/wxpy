#coding=utf-8
'''
import socket
from socket import *

sk=socket(AF_INET,SOCK_STREAM)
addr=('127.0.0.1',9990)
sk.bind(addr)
sk.listen(5)

while True:
    print('waiting for con...')
    c,src=sk.accept()
    while True:
        data=c.recv(1024)
        if not data:
            break
        print(data.decode('utf-8'))
        c.send(bytes('hello world','utf-8'))
        p=input('>')
        if not p:
            break
        c.send(bytes(p,'utf-8'))
    print('cnn from',src)
'''
from twisted.internet import protocol,reactor

port=9992

class tsserver(protocol.Protocol):
    def connectionMade(self):
        cli=self.cli=self.transport.getPeer().host
        print('cnn from',cli)

    def dataReceived(self,data):
        d=data.decode('utf-8')
        print(d)
        self.transport.write(bytes('hello','utf-8')) 

factory=protocol.Factory()
factory.protocol=tsserver
print('waiting for cnn..')
reactor.listenTCP(port,factory)
reactor.run()

