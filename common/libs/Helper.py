# @author : Leo
# @time : 2018/12/16 下午2:30
from flask import g, render_template
from application import app

'''
    统一渲染
'''


def ops_render(template, context={}):
    if 'current_user' in g:
        context['current_user'] = g.current_user

    return render_template(template, **context)
