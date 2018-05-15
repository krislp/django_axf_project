

from django.conf.urls import url
from django.views.static import serve

from axf_app import views
from axf_project import settings

urlpatterns = [
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":settings.STATIC_ROOT}),
    # url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    # 首页
    url(r'^home/', views.home, name='index'),
    # 登陆
    url(r'^login/', views.userLogin, name='login'),
    # 注册
    url(r'^regist/', views.userRegist, name='regist'),
    # 退出登陆
    url(r'^logout/', views.logout, name='logout'),
    url(r'^checkuser/', views.checkuser),
    # 我的
    url(r'^mine/', views.mine, name='mine'),
    # 购物车
    url(r'^cart/', views.cart, name='cart'),

    # 闪购
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)/', views.market_params, name='mparams'),

    # 添加/删除商品
    url(r'^addshop/', views.addShop, name='addshop'),
    url(r'^subshop/',views.subShop, name='subshop'),

    # 改变购物车订单选择状态
    url(r'changeselect', views.changSelect, name='changeselect'),
    url(r'^selectall/', views.selectAll, name='selectall'),

    # 购物车下单
    url(r'^cartorder/', views.cartOrder, name='order'),

    # 支付
    url(r'^topay/(\d+)', views.toPay, name='topay'),

    # 待付款
    url(r'^waitpay/', views.waitPay, name='waitpay'),

    # 待收货
    url(r'^payed/', views.payed, name='payed'),
]
