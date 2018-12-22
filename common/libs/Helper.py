# @author : Leo
# @time : 2018/12/16 下午2:30
from flask import g, render_template
from application import app
import datetime

'''
    统一渲染
'''


def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user

    return render_template(template, **context)
'''
获取当前时间
'''

def createCurrentTime(format = "%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format)

'''
分页
tolal:总数量
page_size:每页数量
page:当前页面
display:展示多少页
'''

def Pagination(params):
    import math

    ret = {
        "is_prev":1,
        "is_next":1,
        "from" :0 ,
        "end":0,
        "current":0,
        "total_pages":0,
        "page_size" : 0,
        "total" : 0,
        "url":params['url']
    }

    total = int(params['total'])
    page_size = int(params['page_size'])
    page = int(params['page'])
    display = int(params['display'])
    total_pages = int(math.ceil(total / page_size))
    total_pages = total_pages if total_pages > 0 else 1
    if page <= 1:
        ret['is_prev'] = 0

    if page >= total_pages:
        ret['is_next'] = 0


    semi = int( math.ceil( display / 2 ) )

    if page - semi > 0 :
        ret['from'] = page - semi
    else:
        ret['from'] = 1

    if page + semi <= total_pages :
        ret['end'] = page + semi
    else:
        ret['end'] = total_pages

    ret['current'] = page
    ret['total_pages'] = total_pages
    ret['page_size'] = page_size
    ret['total'] = total
    ret['range'] = range( ret['from'],ret['end'] + 1 )
    return ret
