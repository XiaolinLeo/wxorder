# @author : Leo
# @time : 2018/12/3 下午7:58
from application import app

'''
拦截器
'''
from web.interceptors.Authinterceptor import *


from web.controls.index import route_index
from web.controls.user.User import route_user
from web.controls.static import route_static
from web.controls.account.Account import route_account
from web.controls.finance.Finance import route_finance

app.register_blueprint(route_index,url_prefix="/")
app.register_blueprint(route_user,url_prefix='/user')
app.register_blueprint(route_static,url_prefix='/static')
app.register_blueprint(route_account,url_prefix='/account')
app.register_blueprint(route_finance,url_prefix='/finance')