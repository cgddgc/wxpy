import weroot,urllib,requests,json


we=werobot.WeRoBot()
we.config.from_pyfile(".weconfig")
we.Client.get_menu()