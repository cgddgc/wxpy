#coding=utf-8
import werobot

token="cgddgc"

robot=werobot.WeRoBot(token=token)
message=robot.Message

@robot.text
def hl(message):
    return Message.content+"蠢材"

@robot.image
def h2():
    return message.img

robot.config['HOST']='0.0.0.0'
robot.config['PORT']=8998
robot.run()