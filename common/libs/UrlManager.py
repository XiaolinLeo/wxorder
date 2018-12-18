# @author : Leo
# @time : 2018/12/4 下午7:45

'''
版本链接统一管理
'''
class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s" % (22222222)
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)
