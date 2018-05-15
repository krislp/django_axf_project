import time
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from axf_app.models import UserModel, UserTicket


# 中间件 当用户进入我的和购物车页面时验证用户是否登陆
# 此处知识给request绑定user，所以在我的和购物车views中需要判断request中是否存在user
class UserLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # 获取浏览器 ticket
        ticket = request.COOKIES.get('ticket')
        # 若浏览器中没有ticket 说明没有用户登陆过 不做任何操作 继续执行url
        if not ticket:
            return None
        # 若浏览器中存在 ticket 说明用户登陆过 判断 ticket 是否过期
        userticket = UserTicket.objects.filter(ticket=ticket)
        # 判断 数据库中 ticket 时间是否过期
        if userticket[0].out_time < time.time():
            userticket.delete()
        else:
            # 若ticket 未过期 把 user 绑定在 request 中
            request.user = userticket[0].user