#!python3
#coding=utf-8
import urllib,urllib.parse,urllib.request,sys,io,json,re,random,base64,os,requests,bs4
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from wxcfg import GlobalConfig

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class cloud_music():
    def __init__(self):
        self.agents=[
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0"
        ]
        self.header=[('Origin','http://music.163.com'),('User-Agent', random.choice(self.agents)),('Referer','http://music.163.com')]
        self.search_url='http://music.163.com/api/search/get/'
        self.detail_url='http://music.163.com/weapi/song/enhance/player/url?csrf_token='

    def enc(self,data):
        key1="0CoJUm6Qyw8W8jud"
        vi="0102030405060708"
        key2="a8LWv2uAtXjzSfkQ" 
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        encry1=AES.new(key1,AES.MODE_CBC,vi)
        param=str(base64.b64encode(encry1.encrypt(pad(data))),encoding='utf-8')
        encry2=AES.new(key2,AES.MODE_CBC,vi)
        param=str(base64.b64encode(encry2.encrypt(pad(param))),encoding='utf-8')
        encSecKey='2d48fd9fb8e58bc9c1f14a7bda1b8e49a3520a67a2300a1f73766caee29f2411c5350bceb15ed196ca963d6a6d0b61f3734f0a0f4a172ad853f16dd06018bc5ca8fb640eaa8decd1cd41f66e166cea7a3023bd63960e656ec97751cfc7ce08d943928e9db9b35400ff3d138bda1ab511a06fbee75585191cabe0e6e63f7350d6'
        return param,encSecKey


    def get_ip(self):  
        url="http://www.xicidaili.com/nn"  
        headers = {"Accecpt":"text/html,application/xhtml+xml,application/xml",  
                    "Accept-Encoding":"gzip,deflate,sdch",  
                    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",  
                    "Referer":"http://www.xicidaili.com",  
                    "User-Agent":"Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"  
                    }  
        r = requests.get(url,headers=headers)  
        soup =bs4.BeautifulSoup(r.text,'html.parser')  
        data=soup.table.find_all("td")  
        ip_compile=re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  
        port_compile=re.compile(r"<td>(\d+)</td>")  
        ip=re.findall(ip_compile,str(data))  
        port=re.findall(port_compile,str(data))
        res=[":".join(i) for i in zip(ip,port)]
        #print(random.choice(res)) 
        return res


    def get_music(self,keyword='采茶纪'):
        #code=''
        art=''
        sname=keyword
        #info=''
        try:
            if not keyword=="":
                if (keyword.find('*')>=0):
                    #print(keyword.find('*'))
                    sname=keyword[0:keyword.find('*')]
                    art=keyword[keyword.find('*')+1:len(keyword)]
                    #print(name,art)
                else:
                    pass
                data={'s':sname,'offset':'0','limit':'10','type':'1'}
                data=urllib.parse.urlencode(data).encode('utf-8')
                req=urllib.request.Request(self.search_url,data)
                req.addheaders=self.header
                res=urllib.request.urlopen(req).read()
                song=json.loads(res)['result']#['songs'][0]
                #print(song['songs'][9]['artists'][0]['name'])
                if 'songs' in song:
                    id=0
                    #code=self.get_info(song['songs'][0])
                    #print(len(song['songs']))
                    for i in range(len(song['songs'])):
                        artist=song['songs'][i]['artists'][0]['name']
                        if art in artist:
                            id=i
                            break
                        else:
                            pass
                    code=self.get_info(song['songs'][i])
                    #print(code)
                elif ('songCount' in song and song['songCount']==0):
                    code='什么都没找到，换一首吧'

                else:
                    code='未知错误'     
            else:
                code='关键字不能为空'
        except Exception as e:
            code=e
        #print(code)
        return code


    def get_info(self,song):
        muid=song['id']
        data1={'ids':'['+str(muid)+']','br':3200000,'csrf_token':''}
        params,encSecKey=self.enc(json.dumps(data1))
        post={'params':params,'encSecKey':encSecKey}
        data1=urllib.parse.urlencode(post).encode('utf-8')
        #print(data1)
        proxy=GlobalConfig.Myproxy
        proxy_handler=urllib.request.ProxyHandler(proxy)
        opener=urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
        req=urllib.request.Request(self.detail_url,data1)
        req.addheaders=self.header
        #print(header)
        res=urllib.request.urlopen(req).read().decode('utf-8')
        #print(res1)
        out=json.loads(res)['data'][0]
        info={'name':song['name'],'artists':song['artists'][0]['name'],'album':song['album']['name'],'url':out['url']}
        #print(out)
        return info

#'''
if __name__ == '__main__':
    #data={'ids':'['+'41500546'+']','br':3200000,'csrf_token':''}
    #data={"ids":"[484730184]","br":128000,"csrf_token":""}
    #enc(json.dumps(data))
    #m=cloud_music()
    #m.get_music()
    #get_ip()
    pass