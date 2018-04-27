#!coding=utf-8
import time,pymysql,json,requests,os,subprocess
from cloud_music import cloud_music
from Crypto.Cipher import AES
from wxcfg import GlobalConfig,DefaultResponseMsg
import weclient as wc

def get_user_status(message,session):
    key=message.content
    if 'status' in session:
        if DefaultResponseMsg.musicMode==key:
            session['mode']='change_mode'
            session['status']='music_mode'
        elif DefaultResponseMsg.chatMode==key:
            session['mode']='change_mode'
            session['status']='chat_mode'
        elif DefaultResponseMsg.commanMode==key:
            session['mode']='change_mode'
            session['status']='comman_mode'
        else:
            session['mode']='auto_mode'
            #session['status']='chat_mode'
    else:
        session['status']='chat_mode'
        session['mode']='auto_mode'
    return session['status'],session['mode']

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
            res=DefaultResponseMsg.noMusicUrl
    else:
        res=info
        #print(res)
    return res

def shell_exec(message,key):
    if message.source in GlobalConfig.owner:
        key=key.replace('执行','')
        res=subprocess.getoutput(key)
    else:
        res=DefaultResponseMsg.noPermission
    return res

def get_user_want(key):
    if '~' in key or '来首' in key:
        return 'get_music'
    elif 'openid' in key:
        return 'get_openid'
    elif '访问情况' in key:
        return 'get_status'
    else:
        return 'chat'

def get_req_num(message,n):
    if message.source in GlobalConfig.owner:
        ipnum_sh='tail -'+str(n)+' /var/log/httpd/access_log|awk \'{print $1}\'|sort|uniq -c|sort -k1nr|head -10'
        res=os.popen(ipnum_sh,'r').read()
        #res=os.system(ipnum_sh)
        #print(res,type(res))
        resp='最近500次访问中访问前10的ip地址如下:\n'+str(res)
        #wc.sent_notice('\n'+res,'server')
    else:
        resp=DefaultResponseMsg.noPermission
    return resp


def action(a,message):
    if a=='get_music':
        return reply_music(message.content)
    elif a=='get_openid':
        return message.source
    elif a=='chat':
        return TulingRobot(message.content,message.source)
    elif a=='get_status':
        return get_req_num(message,500)
    else:
        return 'error'

def mode(a,message,des):
    if a=='chat_mode':
        return action(des,message)
    elif a=='music_mode':
        return reply_music(message.content)
    elif a=='comman_mode':
        return shell_exec(message,message.content)
    else:
        return 'error'

def respon(a,stat,des,message):
    if a=='change_mode':
        return stat
    elif a=='auto_mode':
        return mode(stat,message,des)
    else:
        return 'error'