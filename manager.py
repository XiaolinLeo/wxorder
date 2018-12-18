# @author : Leo
# @time : 2018/12/3 下午7:58
from application import app,manager

from flask_script import Server

import sys
import traceback
import www
#Webserver
manager.add_command("runserver",Server(host="127.0.0.1",port=app.config["SERVER_PORT"],use_debugger=True))

def main():
    manager.run()


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
#错误打印
        traceback.print_exc()