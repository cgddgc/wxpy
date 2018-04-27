#coding=utf-8
import werobot,urllib,requests,json,re,random,urllib.parse,urllib.request,sys,base64,os,types,time,pymysql
import util
from wxcfg import RobotConfig,cgddgcConfig,DefaultResponseMsg


robot=werobot.WeRoBot()
cgddgc=werobot.WeRoBot()

robot.config.from_object(RobotConfig)
cgddgc.config.from_object(cgddgcConfig)

@robot.text
@cgddgc.text
def responText(message):
    util.record(message.source,message.content,time.strftime('%Y-%m-%d %H:%M:%S'))
    key=message.content
    #stat,stat_mode=util.get_user_status(message,session)
    des=util.get_user_want(key)
    '''
    action={'get_music':util.reply_music(key),
    'get_openid':message.source,
    'chat':util.TulingRobot(key,message.source),
    'get_status':util.get_req_num(message,500)}

    mode={'chat_mode':action[des],
    'music_mode':util.reply_music(key),
    'comman_mode':util.shell_exec(message,key),
    }

    respon={'change_mode':stat,
    'auto_mode':mode[stat]}
    '''  
    #print(des)
    return util.action(des,message)
    #return util.respon(stat_mode,stat,des,message)

@robot.voice
@cgddgc.voice
def respon_voice(message):
    key=message.recognition
    util.record(message.source,message.recognition,time.strftime('%Y-%m-%d %H:%M:%S'))
    des=util.get_user_want(key)
    action={'get_music':util.reply_music(key),
    'get_openid':message.source,
    'chat':util.TulingRobot(key,message.source),
    'get_status':util.get_req_num(500)}
    return action[des]

@robot.subscribe
@cgddgc.subscribe
def subscribe(message):
    return DefaultResponseMsg.subscribe

@robot.image
def resp2(message):
    return message.img

@robot.location
def resp3(message):
    return message.label

if __name__ == '__main__':
    robot.run()
