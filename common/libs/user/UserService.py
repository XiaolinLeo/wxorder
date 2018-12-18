# @author : Leo
# @time : 2018/12/14 下午12:09
import hashlib, base64




class UserService():
    #cookie加密
    @staticmethod
    def geneAuthCode(user_info):
        m = hashlib.md5()
        str = "%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    # 登录密码加密校验
    @staticmethod
    def getPwd(pwd, salt):
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

