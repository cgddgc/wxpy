import werobot,urllib,requests,json


we=werobot.WeRoBot()
we.config.from_pyfile(".weconfig")
print(we.client.get_menu())