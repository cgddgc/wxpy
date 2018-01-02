#!coding=utf-8
import pymysql
class GlobalConfig():
    dbconf={'host':'127.0.0.1','port':3306,'user':'gxd','password':'cgd626723','db':'wechat','charset':'utf8','cursorclass':pymysql.cursors.DictCursor}
    TulingKey="b8bb8bf591af8b522652fc2aa1e4a03a"
    Myproxy={"http":"120.78.156.241:6666"}

class RobotConfig():
    TOKEN="cgddgc"
    SERVER="auto"
    HOST="0.0.0.0"
    PORT=8998
    SESSION_STORAGE=None
    APP_ID="wx03b529f87a6d25a7"
    APP_SECRET="678d29e1b19f6e5a3beb110e9699b136"
    ENCODING_AES_KEY=None
