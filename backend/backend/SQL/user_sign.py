from .base_sql import Basic_opear as sql
from . import settings

# 暂为多电脑可同时登录一个账户
# 后期更新


class sign(object):

    #检查账户密码是否正确
    def check_account(self,account,passwd):
        sign = sql().check_exist(settings.USER_INFO,settings.ACCOUNT,{"account":account,"passwd":passwd})
        if(sign):
            return True
        else:
            return False

    #更新用户cookie
    def Change_cookie(self,account,cookie):
        cookie_sign = sql().check_exist(settings.USER_INFO,settings.COOKIE,{"cookie":cookie})
        if(cookie_sign):
            sql().update(settings.USER_INFO,settings.COOKIE,{"cookie":cookie},{"account":account})
        else:
            sql().insert(settings.USER_INFO,settings.COOKIE,{"account":account,"cookie":cookie})

    def main(self,account,passwd,cookie):
        if(self.check_account(account,passwd)):
            self.Change_cookie(account,cookie)
            return True
        else:
            return False
