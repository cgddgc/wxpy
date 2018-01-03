#!coding=utf-8
from flask import Flask,request
from wechat import robot
from werobot.contrib.flask import make_view
import weclient as wc
from wxcfg import RobotConfig


app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def response():
    if request.method=='POST':
        user=request.form['user']
        pwd=request.form['pwd']
        wc.sent_notice(user,pwd)
        return user+pwd
    else:
        return 'error'

robot.config.from_object(RobotConfig)
app.add_url_rule(rule='/werobot/',endpoint='robot',view_func=make_view(robot),methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0')
