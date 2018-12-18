# @author : Leo
# @time : 2018/12/4 下午7:14
from flask import Blueprint, request, jsonify, redirect, make_response, render_template,g

from common.models.User import User

from common.libs.Helper import ops_render
from common.libs.user.UserService import UserService
from common.libs.UrlManager import UrlManager
from application import app,db

import json

route_user = Blueprint('user_page', __name__)


@route_user.route("/login", methods=["GET", "POST"])
def login():
    resp = {'code': 0}
    if request.method == "GET":
        return render_template('user/login.html',info=resp)
    # 接受传过来的用户名密码
    req = request.values
    login_name = req["login_name"] if 'login_name' in req else ''
    login_pwd = req["login_pwd"] if 'login_pwd' in req else ''

    # 检验用户名密码

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名或密码'
        return render_template('user/login.html', info=resp)
    if login_pwd is None or len(login_pwd) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名或密码'
        return render_template('user/login.html', info=resp)
    # 从数据库中查询

    user_info = User.query.filter_by(login_name=login_name).first();
    if not user_info:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名或密码'
        return render_template('user/login.html', info=resp)
    # 校验密码
    if user_info.login_pwd != UserService.getPwd(login_pwd, user_info.login_salt):
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名或密码'
        return render_template('user/login.html', info=resp)

    # response = make_response(json.dumps(resp))
    resp['code'] = 200
    resp['msg'] = '登录成功'
    response = make_response(redirect(UrlManager.buildUrl('/')))
    response.set_cookie(app.config["USER_COOKIE_AUTH_NAME"],
                        "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid),60*60*24)
    return response


@route_user.route('/logout')
def logout():
    response = make_response(redirect(UrlManager.buildUrl('/user/login')))
    response.delete_cookie(app.config['USER_COOKIE_AUTH_NAME'])
    return response


@route_user.route('/edit',methods=["GET","POST"])
def edit():
    resp = {'code': 0,'current':'edit'}
    if request.method == 'GET':
        return ops_render('user/edit.html', resp)

    req = request.values
    nickname = req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) <1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的用户名～"
        return ops_render('user/edit.html',resp)
    #邮箱校验还有问题,判断是否是邮箱
    if email is None or len(email) <1:
        resp['code'] = -2
        resp['msg'] = "请输入符合规范的邮箱～"
        return ops_render('user/edit.html',resp)

    user_info = g.current_user
    user_info.nickname = nickname
    user_info.email = email

    db.session.add(user_info)
    db.session.commit()
    resp['code'] = 1
    resp['msg'] = "修改成功"
    return ops_render('user/edit.html',resp)



@route_user.route('/reset_pwd',methods=["GET","POST"])
def reset_pwd():
    resp={'code':0,'current':'reset_pwd'}
    if request.method == "GET":
        return ops_render('/user/reset_pwd.html',resp)
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''

    if old_password is None or len(old_password) < 5:
        resp['code'] = -1
        resp['msg'] = "请输入正确的旧密码1～"

        return ops_render('user/reset_pwd.html', resp,)

    user_info = g.current_user
    if user_info.login_pwd != UserService.getPwd(old_password,user_info.login_salt) :
        resp['code'] = -2
        resp['msg'] = "请输入正确的旧密码2～"
        return ops_render('user/reset_pwd.html', resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入正确的新密码～"
        return ops_render('user/reset_pwd.html', resp)

    if old_password == new_password:
        resp['code'] = -1
        resp['msg'] = "新密码和原密码不能相同～"
        # return jsonify(resp)
        return ops_render('user/reset_pwd.html', resp)


    user_info.login_pwd = UserService.getPwd(new_password,user_info.login_salt)
    db.session.add(user_info)
    db.session.commit()
    resp['code'] = 1
    resp['msg'] = '修改成功'
    #解决修改密码后重新登录问题
    response = make_response(ops_render('/user/reset_pwd.html',resp))
    response.set_cookie(app.config["USER_COOKIE_AUTH_NAME"],
                        "%s#%s" % (UserService.geneAuthCode(user_info), user_info.uid), 60 * 60 * 24)
    return response


