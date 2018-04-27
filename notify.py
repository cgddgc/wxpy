#!coding=utf-8
import os
import weclient as wc


def get_req_num(n):
    ipnum_sh='tail -'+str(n)+' /var/log/httpd/access_log|awk \'{print $1}\'|sort|uniq -c|sort -k1nr|head -10'
    res=os.popen(ipnum_sh,'r').read()
    #res=os.system(ipnum_sh)
    #print(res,type(res))
    resp='最近500次访问中访问前10的ip地址如下:\n'+str(res)
    #wc.sent_notice('\n'+res,'server')
    return resp
if __name__ == '__main__':
    get_req_num(500)