#!python3
#coding=utf-8
import urllib,urllib.parse,urllib.request,sys,io,json,re,random,base64,os,requests,bs4,pymysql,requests,time,binascii
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from wxcfg import GlobalConfig
from builtins import pow

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class cloud_music():
    def __init__(self):
        self.agents=GlobalConfig.agents
        self.header=[('Origin','http://music.163.com'),('User-Agent', random.choice(self.agents)),('Referer','http://music.163.com')]
        self.search_url='http://music.163.com/api/search/get/'
        self.detail_url='http://music.163.com/weapi/song/enhance/player/url?csrf_token='

    def enc(self,data):
        key1="0CoJUm6Qyw8W8jud"
        vi="0102030405060708"
        seed='1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        p='010001'
        m='00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        k=[]
        for i in range(16):
            r=random.choice(seed)
            k.append(r)
        key2=''.join(k)
        #key2="a8LWv2uAtXjzSfkQ" 
        #pub=rsa.key.PublicKey(int(m,16),int(p,16))
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        encry1=AES.new(key1,AES.MODE_CBC,vi)
        param=str(base64.b64encode(encry1.encrypt(pad(data))),encoding='utf-8')
        encry2=AES.new(key2,AES.MODE_CBC,vi)
        param=str(base64.b64encode(encry2.encrypt(pad(param))),encoding='utf-8')
        #f=binascii.hexlify(rsa.encrypt(key2[::-1].encode('utf-8'),pub)).decode('utf-8')
        e=pow(int(binascii.hexlify(key2[::-1].encode('utf-8')), 16), int(p, 16), int(m, 16))
        e=format(e, 'x').zfill(256)
        #print(key2+'\n',e)
        return param,e


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
        info={'sid':song['id'],'name':song['name'],'artists':song['artists'][0]['name'],'album':song['album']['name'],'url':out['url']}
        #print(info)
        if not (info['url']=='' or info['url']==None):
        #    status_code=200
        #    try:
        #        res=requests.get(info['url'])
        #        status_code=res.status_code
        #    except Exception as e:
        #        print(e)
        #    if not (status_code==404 or status_code=='404'):
            self.record_music(info)
        else:
            pass
        return info

    def record_music(self,info):
        config=GlobalConfig.dbconf
        cnn=pymysql.connect(**config)
        with cnn.cursor() as cursor:
            sec='select sid from music where sid=%s and name=%s and artist=%s and album=%s'
            cursor.execute(sec,(info['sid'],info['name'],info['artists'],info['album']))
            result=cursor.fetchall()
            if not len(result):
                ins='insert into music(sid,name,artist,album,url,update_time) values(%s,%s,%s,%s,%s,%s)'
                cursor.execute(ins,(info['sid'],info['name'],info['artists'],info['album'],info['url'],time.strftime('%Y-%m-%d %H:%M:%S')))
            else:
                upd='update music set url=%s,update_time=%s where sid=%s'
                cursor.execute(upd,(info['url'],time.strftime('%Y-%m-%d %H:%M:%S'),result[0]['sid']))
        cnn.commit()
        cnn.close()

#'''
if __name__ == '__main__':
    #data={'ids':'['+'41500546'+']','br':3200000,'csrf_token':''}
    #data={"ids":"[484730184]","br":128000,"csrf_token":""}
    #enc(json.dumps(data))
    #m=cloud_music()
    #m.get_music()
    #get_ip()
    pass