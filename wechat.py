#coding=utf-8
import werobot

token="cgddgc"

robot=werobot.WeRoBot(token=token)

@robot.text
def hl(message):
    return message.content+"蠢材"

@robot.image
def h2(message):
    return message.img
@robot.event
def echoevent(message):
    return message.event
robot.config['HOST']='0.0.0.0'
robot.config['PORT']=8998
robot.run()