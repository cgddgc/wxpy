#!python3
#!coding=utf-8 

from http.server import HTTPServer,BaseHTTPRequestHandler     
import io,shutil,urllib,json     

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
        print(pstr["signature"][0],pstr["nonce"][0],pstr["timestamp"][0])
        #s=str(self.rfile.readline().decode(),'utf-8')  
        #s=self.rfile.readline().decode()
        s=self.request.recv(2048).strip()
        print(s)
        #print(urllib.parse.parse_qs(urllib.parse.unquote(s)))
        self.send_response(301)
pyhttpd=HTTPServer(('',8998),MyHttpHandler)     
print("Server started on 127.0.0.1,port 8998.....")     
pyhttpd.serve_forever()