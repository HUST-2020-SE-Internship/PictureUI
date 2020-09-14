from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from users import models


# 全局登录中间件
class UserLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 用==比较str是否相等竟然失败了???只好用__contains__了!
        for open_path in settings.GATE_URL:
            if request.path.__contains__(open_path):
                return None

        logged_user_id = request.session.get('_auth_user_id')

        if not logged_user_id:
            request.session['redirect_from_auth'] = True
            return HttpResponseRedirect('/users/login')
        