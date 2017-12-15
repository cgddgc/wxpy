#coding=utf-8
import werobot

token="cgddgc"

robot=werobot.WeRoBot(token=token)

@robot.text
def hl():
    return "蠢材"


robot.run()