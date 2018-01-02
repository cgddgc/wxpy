#!coding=utf-8
import time,pymysql,json,requests

def record(user,content,time):
    config={'host':'127.0.0.1','port':3306,'user':'gxd','password':'cgd626723','db':'wechat','charset':'utf8','cursorclass':pymysql.cursors.DictCursor}
    cnn=pymysql.connect(**config)
    with cnn.cursor() as cursor:
        sql='insert into record(openid,text,time) values (%s,%s,%s)'
        res=cursor.execute(sql,(user,content,time))
    cnn.commit()
    cnn.close()

def TulingRobot(word,user):
    url = "http://www.tuling123.com/openapi/api"
    r = requests.post(url, data={'key':"b8bb8bf591af8b522652fc2aa1e4a03a",'info':word,'userid':user})
    result=(json.loads((r.text))["text"])
    return result

def reply_music(key):
    music=cloud_music()
    info=music.get_music(key)
    #print(info)
    if isinstance(info,list) or isinstance(info,dict):
        title=info['artists']+' - '+info['name']
        disc=info['album']
        murl=info['url']
        if not (murl=='' or murl==None):
            res=[
            title,
            disc,
            murl,
            ]
            return res
        else:
            res='啊哦，什么都没找到，可能服务器开小差了，要不换一首吧'
    else:
        res=info
    return res

