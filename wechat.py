#coding=utf-8
import werobot,urllib,requests,json,re,random,urllib.parse,urllib.request,sys,base64,os
from wxcfg import MyConfig
from Crypto.Cipher import AES
from cloud_music import enc,get_mu

robot=werobot.WeRoBot(token="cgddgc")

#robot.config.from_pyfile("wxcfg.py")
#robot.config.from_object(MyConfig)
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=8998


def TulingRobot(message):
    url = "http://www.tuling123.com/openapi/api"#'http://www.xiaodoubi.com/bot/chat.php'
    r = requests.post(url, data={'key':"b8bb8bf591af8b522652fc2aa1e4a03a",'info':message.content,'userid':message.source})
    result=(json.loads((r.text))["text"])
    return result

@robot.text
def responText(message):
    key=message.content
    if (key.find("~")==0):
        info=get_mu(key)
        print(info)
        title=info['artists']+' - '+info['name']
        disc=info['album']
        murl='http://m10.music.126.net/20171227182732/5c7858108268bd85a07e44a8d1177c2e/ymusic/2c40/f980/8761/4c1a1719efcd49f64b504922c082a45b.mp3'#info['url']
        res=[
        title,
        disc,
        murl,
        ]
        print(res)
        return res
    else:
        return TulingRobot(message)

@robot.image
def resp2(message):
    return message.img

@robot.location
def resp3(message):
    return message.label


robot.run()