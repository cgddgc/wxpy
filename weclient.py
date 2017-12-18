import werobot,urllib,requests,json
from wxcfg import MyConfig

we=werobot.WeRoBot()
we.config.from_object(MyConfig)
print(we.client.get_menu())