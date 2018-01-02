import werobot,urllib,requests,json
from wxcfg import MyConfig

we=werobot.WeRoBot()
we.config.from_object(MyConfig)
#print(we.client.get_menu())
#we.client.delete_menu()

#we.client.create_menu({'button':[{ "type":"click","name":"今日歌曲","key":"V1001_TODAY_MUSIC"},
        {"type":"click","name":"歌手简介","key":"V1001_TODAY_SINGER"},
        {"name":"菜单", "sub_button":[{"type":"view","name":"搜索","url":"http://www.soso.com/"},{ "type":"view", "name":"视频", "url":"http://v.qq.com/"},{"type":"click","name":"赞一下我们","key":"V1001_GOOD"}]}]})