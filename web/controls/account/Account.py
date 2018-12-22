# @author : Leo
# @time : 2018/12/12 下午10:16
from flask import Blueprint, redirect, request

from common.libs.Helper import ops_render, createCurrentTime,Pagination
from common.models.User import User

from common.libs.user.UserService import UserService

from common.libs.UrlManager import UrlManager

from application import app, db

route_account = Blueprint('account_page', __name__)


@route_account.route('/index')
def index():
    resp_data = {}
    count = User.query.count()
    req = request.values
    page = int(req['p'] if 'p' in req and req['p'] else 1)
    page_params = {
        'total':count,
        'page_size':app.config['PAGE_SIZE'],
        'page':page,
        'display':app.config['PAGE_DISPLAY'],
        'url':request.full_path.replace("&p={}".format(page),"")
    }
    pages = Pagination(page_params)
    offset = (page - 1) *app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page
    lists = User.query.order_by(User.uid.desc()).all()[offset:limit]
    resp_data['lists'] = lists
    resp_data['pages'] = pages
    return ops_render('/account/index.html', resp_data)


@route_account.route('/info')
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id', 0))
    if uid < 0:
        return redirect(UrlManager.buildUrl('/account/index'))
    info = User.query.filter_by(uid=uid).first()
    if not info:
        return redirect(UrlManager.buildUrl('/account/index'))

    resp_data['info'] = info
    return ops_render('/account/info.html', resp_data)


@route_account.route('/set', methods=['GET', 'POST'])
def set():
    resp = {'code': 0}
    default_pwd = "******"
    if request.method == 'GET':
        resp_data = {}
        #根据传过来的id判断用户是新增还是修改用户
        req = request.args
        uid = req.get("id", 0)
        user_info = None
        if uid:
            user_info = User.query.filter_by(uid=uid).first()
        resp_data['user_info'] = user_info

        return ops_render('/account/set.html',resp_data)

    req = request.values

    id = req['id'] if 'id' in req else ''

    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return ops_render('account/set.html', resp)

    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的手机号'
        return ops_render('account/set.html', resp)

    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的邮箱'
        return ops_render('account/set.html', resp)

    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的密码'
        return ops_render('account/set.html', resp)

    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入符合规范的姓名'
        return ops_render('account/set.html', resp)

    has_in = User.query.filter(User.login_name == login_name,User.uid!=id ).first()
    if has_in:
        resp['code'] = -1
        resp['msg'] = '用户名重复'
        return ops_render('account/set.html', resp)
    user_info = User.query.filter_by(uid = id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = createCurrentTime()
        model_user.login_salt = UserService.geneSalt()
    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    if login_pwd != default_pwd:
        model_user.login_pwd = UserService.getPwd(login_pwd, model_user.login_salt)


    model_user.updated_time = createCurrentTime()

    db.session.add(model_user)
    db.session.commit()
    resp['code'] = 1
    resp['msg'] = "操作成功"
    #return ops_render('account/set.html', resp)
    return redirect(UrlManager.buildUrl('/account/index'))
