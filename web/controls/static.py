# @author : Leo
# @time : 2018/12/12 下午8:56
from flask import Blueprint,send_from_directory
from application import app
route_static = Blueprint('static',__name__)
@route_static.route("/<path:filename>")
def index(filename):
    app.logger.info(filename)
    return send_from_directory(app.root_path+"/web/static/",filename )
