#coding=utf-8
import werobot,urllib,requests,json,re,random,urllib.parse,urllib.request,sys,base64,os,types,time,pymysql
import util
from wxcfg import RobotConfig


robot=werobot.WeRoBot()

robot.config.from_object(RobotConfig)

@robot.text
def responText(message):
    util.record(message.source,message.content,time.strftime('%Y-%m-%d %H:%M:%S'))
    key=message.content
    des=util.get_user_want(key)
    if des=='get_music':
        return util.reply_music(key)
    elif des=='get_openid':
        return message.source
    elif des=='chat':
        return util.TulingRobot(key,message.source)
    else:
        return 'unexpected error'

@robot.voice
def respon_voice(message):
    key=message.recognition
    util.record(message.source,message.recognition,time.strftime('%Y-%m-%d %H:%M:%S'))
    if des=='get_music':
        return util.reply_music(key)
    elif des=='get_openid':
        return message.source
    elif des=='chat':
        return util.TulingRobot(key,message.source)
    else:
        return 'unexpected error'

@robot.subscribe
def subscribe(message):
    return '谢谢关注，发送~或来首+歌名点歌，歌名后可加*指定歌手，发送文字或语音可以和我尬聊'

@robot.image
def resp2(message):
    return message.img

@robot.location
def resp3(message):
    return message.label

if __name__ == '__main__':
    robot.run()
