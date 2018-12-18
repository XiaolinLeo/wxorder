# @author : Leo
# @time : 2018/12/14 上午10:27
from flask import Blueprint,render_template

from common.libs.Helper import ops_render
route_finance = Blueprint('finance_page',__name__)

@route_finance.route('/index')
def index():
    return ops_render('/finance/index.html')
@route_finance.route('/account')
def account():
    return  ops_render('/finance/account.html')

@route_finance.route('/pay-info')
def pay_info():
    return  ops_render('/finance/pay_info.html')