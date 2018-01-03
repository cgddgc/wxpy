import werobot,urllib,requests,json
from wxcfg import RobotConfig
we=werobot.WeRoBot()
we.config.from_object(RobotConfig)
#print(we.client.get_menu())
#we.client.delete_menu()

#we.client.create_menu({'button':[{ "type":"click","name":"今日歌曲","key":"V1001_TODAY_MUSIC"},{"type":"click","name":"歌手简介","key":"V1001_TODAY_SINGER"},{"name":"菜单", "sub_button":[{"type":"view","name":"搜索","url":"http://www.soso.com/"},{ "type":"view", "name":"视频", "url":"http://v.qq.com/"},{"type":"click","name":"赞一下我们","key":"V1001_GOOD"}]}]})
#users=we.client.get_followers()
#print(users)
'''
token=we.client.get_access_token()
ip=we.client.get_ip_list()
a=requests.get('https://api.weixin.qq.com/cgi-bin/template/get_industry?access_token='+token)
print(token,ip['ip_list'][0],a)
'''
def sent_notice(arg1,arg2):
    openid=we.client.get_followers()['data']['openid'][0]
    tid='z5L8q2R1XUlWUNk9y-dwFOvdNx0dfqHIb9JmXILNKps'
    data={'first':{'value':'Warming!\n\n','color':'#FF0000'},'keyword1':{'value':arg1+'\n','color':'#FF0000'},'keyword2':{'value':arg2+'\n','color':'#FF0000'},'remark':{'value':'\n注意','color':'#FF0000'}}
    url='https://blog.cgddgc.cn'
    res=we.client.send_template_message(openid,tid,data,url)
    print(openid,res)