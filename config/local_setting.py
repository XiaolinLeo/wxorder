# @author : Leo
# @time : 2018/12/3 下午7:35
DEBUG = True
SQLALCHEMY_ENCODING = "utf-8"
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1/food_db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

USER_COOKIE_AUTH_NAME = "food"
'''
不需要过滤的URL
'''
IGNORE_URLS = [
    "^/user/login"
]

IGNORE_STATIC_URLS = [
    "^/static",
    "^/favicon.ico"
]

'''
分页配置
'''

PAGE_SIZE = 1
PAGE_DISPLAY = 10