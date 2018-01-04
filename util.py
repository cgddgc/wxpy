#!coding=utf-8
import time,pymysql,json,requests
from cloud_music import cloud_music
from Crypto.Cipher import AES
from wxcfg import GlobalConfig

def record(user,content,time):
    config=GlobalConfig.dbconf
    cnn=pymysql.connect(**config)
    with cnn.cursor() as cursor:
        sql='insert into record(openid,text,time) values (%s,%s,%s)'
        res=cursor.execute(sql,(user,content,time))
    cnn.commit()
    cnn.close()

def TulingRobot(word,user):
    url = "http://www.tuling123.com/openapi/api"
    r = requests.post(url, data={'key':GlobalConfig.TulingKey,'info':word,'userid':user})
    result=(json.loads((r.text))["text"])
    return result

def reply_music(key):
    music=cloud_music()
    key=key.replace("~","").replace('来首','')
    info=music.get_music(key)
    if isinstance(info,list) or isinstance(info,dict):
        title=info['artists']+' - '+info['name']
        disc=info['album']
        murl=info['url']
        if not (murl=='' or murl==None):
            res=[title,disc,murl,]
            return res
        else:
            res='啊哦，什么都没找到，可能服务器开小差了，要不换一首吧'
    else:
        res=info
        #print(res)
    return res

def get_user_want(key):
    if '~' in key or '来首' in key:
        return 'get_music'
    elif 'openid' in key:
        return 'get_openid'
    else:
        return 'chat'