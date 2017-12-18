import werobot,urllib,requests,json


we=werobot.WeRoBot()
we.config.from_pyfile(".weconfig")
print(we.Client.get_menu())