#coding=utf-8
import werobot

token="cgddgc"

robot=werobot.WeRoBot(token=token)
robot.config.update(HOST='0.0.0.0',PORT=8998)

@robot.text
def hl():
    return "蠢材"


robot.run()