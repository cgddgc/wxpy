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
def sent_notice(arg1,k='msg'):
    kind={'server':'a_K0T4-Xu0UtEfBCfcKfX8F6fkpN2sPXsT30Wmpm-B4','notice':'z5L8q2R1XUlWUNk9y-dwFOvdNx0dfqHIb9JmXILNKps','msg':'jl0Dh49b7gj-hPWmKDxAKAyWIKSbf0SFFoxNWAXPrOU'}
    #openid=we.client.get_followers()['data']['openid'][0]
    #openid='oVdu6swIuCYPoiKN6NGXz2UAxmmo'
    openid='oVdu6swIuCYPoiKN6NGXz2UAxmmo'
    tid=kind[k]
    #data={'first':{'value':'Warming!\n\n','color':'#FF0000'},'keyword1':{'value':arg1+'\n','color':'#FF0000'},'keyword2':{'value':k+'\n','color':'#FF0000'},'remark':{'value':'\n注意','color':'#FF0000'}}
    #data={'first':{'value':'访问情况如下：\n','color':'#000000'},'keyword1':{'value':arg1+'\n','color':'#000000'},'remark':{'value':'\nEND','color':'#000000'}}
    data={'first':{'value':arg1,'color':'#000000'}}
    url='http://wxpy.cgddgc.cn/'
    res=we.client.send_template_message(openid,tid,data,url)
    #print(res)

if __name__ == '__main__':
    sent_notice('hello','server')