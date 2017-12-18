import werobot,urllib,requests,json


we=werobot.WeRobot.Client()
we.config.from_pyfile(".weconfig")
print(we.get_menu())