#!python3
#!coding=utf-8 

from http.server import HTTPServer,BaseHTTPRequestHandler     
import io,shutil,urllib,json,threading,_thread     
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,create_reply
import socket

token='cgddgc'
sock.bind('0.0.0.0',8998)
sock.listen(5)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class MyHttpHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):       
        if '?' in self.path:     
            self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])          
            params=urllib.parse.parse_qs(self.queryString)     
            #print(params)     
        self.send_response(200)             
    def do_POST(self):
        self.queryString=urllib.parse.unquote(self.path.split('?',1)[1])          
        pstr=urllib.parse.parse_qs(self.queryString)
        #signature=pstr["signature"][0]
        #nonce=pstr["nonce"][0]
        #timestam=pstr["timestamp"][0]
        #s=str(self.rfile.readline().decode(),'utf-8')  
        s=self.rfile.readlines()
        #s=self.request.recv(2048).strip()
        l=len(s)
        print(l)
        for i in range(l):
            s[i]=s[i].decode('utf-8')#=s[l-1].decode(encoding='utf-8')
        xml=''
        xml=xml.join(list(s))
        print(xml)
        return pstr,xml
        #print(urllib.parse.parse_qs(urllib.parse.unquote(s)))
        self.send_response(301)

    def valid(self):
        pstr,xml=self.post.do_POST()
        timestamp=pstr["timestamp"][0]
        nonce=pstr["nonce"][0]
        signature=pstr["signature"][0]
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            print('error')
            pass 

    def responMsg(self):
        while 1:
            if(self.do_POST()):
                pstr,xml=self.do_POST()
                msg=parse_message(xml)
                reply = TextReply(message=msg)
                reply.content = 'text reply'
                restr=reply.rener()
                print(msg,restr)
pyhttpd=HTTPServer(('',8998),MyHttpHandler)     
print("Server started on 127.0.0.1,port 8998.....") 
we=MyHttpHandler()    
we.responMsg()
#pyhttpd.serve_forever()

