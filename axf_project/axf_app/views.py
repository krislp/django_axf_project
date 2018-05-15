import random

import time

from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from axf_app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, UserTicket, OrderModel, \
    FoodType, Goods, CartModel, OrderGoodsModel
from utils.functions import create_ticket


# 首页
def home(request):
    data = {
        'wheel': MainWheel.objects.all(),
        'nav': MainNav.objects.all(),
        'mustbuy': MainMustBuy.objects.all(),
        'shop': MainShop.objects.all(),
        'show': MainShow.objects.all(),
    }
    return render(request, 'home/home.html', data)


# 登陆
def userLogin(request):

    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if user.password == password:
                ticket = create_ticket()
                # expires 过期时间，这是个 Unix 时间戳，即从 Unix 纪元开始的秒数。
                # 换而言之，通常用 time() 函数再加上秒数来设定 cookie 的失效期。
                # 或者用mktime()来实现。
                ticket_time = time.time() + 60*60*24
                response = HttpResponseRedirect('/axf/mine/')
                response.set_cookie('ticket', ticket, expires=ticket_time)
                # 有可能出现用户未退出登陆的时候，又进入登陆页面，这时表中还会有ticket信息，只需要更新表中数据
                if UserTicket.objects.filter(user_id=user.id).exists():
                    userticket = UserTicket.objects.filter(user_id=user.id)[0]
                    userticket.out_time = ticket_time
                    userticket.ticket = ticket
                    userticket.save()
                else:
                    # 创建新记录
                    UserTicket.objects.create(
                        user_id=user.id,
                        # user=user[0]
                        ticket=ticket,
                        out_time=ticket_time
                    )
                return response
            else:
                return HttpResponse('密码错误')
        else:
            return render(request, 'user/user_register.html')


# 注册
def userRegist(request):

    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        UserModel.objects.create(
            username=request.POST.get('username'),
            password=request.POST.get('password'),
            email=request.POST.get('email'),
            icon=request.FILES.get('icon')
        )
        return HttpResponseRedirect('/axf/login/')


# 退出登陆
def logout(request):
    if request.method == 'GET':
        # 删除数据库中ticket
        id = request.user.id
        UserTicket.objects.get(user_id=id).delete()
        response = HttpResponseRedirect('/axf/home/')
        # 删除浏览器中的ticket
        response.delete_cookie('ticket')
        return response


# 检查用户名
def checkuser(request):
    username = request.GET.get('username')
    users = UserModel.objects.filter(username=username)
    if not users:
        return None
    else:
        return HttpResponse('用户名已被占用')


# 个人中心
def mine(request):
    if request.method == 'GET':
        data = {}
        if request.user.id:
            # 获取用户的订单信息
            orders = OrderModel.objects.filter(user_id=request.user.id)
            wait_pay, payed = 0, 0
            for i in orders:
                if i.o_status == 0:
                    wait_pay += 1
                else:
                    payed += 1
            data['wait_pay'] = wait_pay
            data['payed'] = payed
        return render(request, 'mine/mine.html', data)


# 闪购
def market(request):

    return HttpResponseRedirect(reverse('axf:mparams', args=('104749', '0', '0')))


# 参数：分类id 子分类id 排序id
def market_params(request, typeid, childcid, storenums):
    data = {}
    foodtypes = FoodType.objects.all()
    childcid_lists = FoodType.objects.filter(typeid=typeid).first()
    childcid_list = []
    for i in childcid_lists.childtypenames.split('#'):
        childcid_list.append(i.split(':'))
    data['foodtypes'] = foodtypes
    data['typeid'] = typeid
    data['childcid_list'] = childcid_list
    data['childcid'] = childcid

    if childcid == '0':
        goods = Goods.objects.filter(categoryid=typeid)
    else:
        goods = Goods.objects.filter(categoryid=typeid, childcid=childcid)

    if storenums == '0':
        pass
    elif storenums == '1':
        goods = goods.order_by('productnum')
    elif storenums == '2':
        goods = goods.order_by('-price')
    elif storenums == '3':
        goods = goods.order_by('price')

    data['goods'] = goods
    return render(request, 'market/market.html/', data)


# 购物车
def cart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            carts = CartModel.objects.filter(user=user)
            data = {
                'carts': carts,
                'total_price': total_price(user),
                'is_select_all': is_select_all(user)
            }
            return render(request, 'cart/cart.html', data)
        else:
            return HttpResponseRedirect('/axf/login/')


# 添加商品
def addShop(request):

    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        goods_id = request.POST.get('goods_id')
        user = request.user
        onecart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        # 该用户已经添加过该商品在购物车
        if onecart:
            onecart.c_num += 1
            onecart.save()
            data['c_num'] = onecart.c_num
        else:
            # 用户未添加该商品在购物车
            CartModel.objects.create(
                user=user,
                goods_id=goods_id,
                c_num=1
            )
            data['c_num'] = 1
        data['total_price'] = total_price(user)
        return JsonResponse(data)


# 减少商品
def subShop(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        onecart = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        if onecart:
            # 商品数量为 1 ，减少商品，数量则为 0 ，需要在购物车模型中删除此条记录
            if onecart.c_num == 1:
                onecart.delete()
                data['c_num'] = 0
            else:
                # 商品数量不为1
                onecart.c_num -= 1
                onecart.save()
                data['c_num'] = onecart.c_num
            data['total_price'] = total_price(user)
        return JsonResponse(data)


# 修改select
def changSelect(request):
    if request.method == 'POST':

        data = {
            'msg': '请求成功',
            'code': '200'
        }

        user = request.user

        if user and user.id:

            # 改变select的值
            cart_id = request.POST.get('cart_id')
            cart = CartModel.objects.filter(pk=cart_id).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select

            # 获取所选择商品的总价
            data['total_price'] = total_price(user)

            # 判断购物车中数据是否全选
            data['is_select_all'] = is_select_all(user)
        return JsonResponse(data)


# 全选
def selectAll(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        user = request.user
        carts_id = []
        if user and user.id:
            # 获取未选择的购物车订单
            carts = CartModel.objects.filter(user=user, is_select=False)
            if carts:
                # 修改未选择的购物车订单的 is_select 值
                for cart in carts:
                    cart.is_select = True
                    cart.save()
                    # JsonResponse 不支持数据序列化
                    # 不能直接把 carts 赋值给data，可以把 cart.id 装在列表中传过去
                    carts_id.append(cart.id)
        data['carts_id'] = carts_id

        # 获取所选购物车订单的总价
        data['total_price'] = total_price(user)
        return JsonResponse(data)


# 下单
def cartOrder(request):
    user = request.user
    if user and user.id:

        # 获取已选择的购物车订单
        select_cart = CartModel.objects.filter(user=user, is_select=True)

        # 创建用户订单表
        order = OrderModel.objects.create(
            user=user,
            # 0 下单未付款
            o_status=0,
            o_number='order_' + orderNumber()
        )
        for cart in select_cart:
            # 创建订单商品表
            OrderGoodsModel.objects.create(
                goods=cart.goods,
                order=order,
                goods_num=cart.c_num
            )
            # 删除购物车模型中的记录
            cart.delete()

        user_orders_goods = OrderGoodsModel.objects.filter(order=order)
        orders_goods = []
        for order_goods in user_orders_goods:
            orders_goods.append(order_goods)

        return render(request, 'order/order_info.html', {'orders_goods': orders_goods, 'order': order})


# 支付
def toPay(request, order_id):

    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))


# 待付款
def waitPay(request):
    if request.method == 'GET':
        user = request.user
        user_orders_goods = order_goods(user, 0)
        return render(request, 'order/order_list_wait_pay.html', {'user_orders_goods': user_orders_goods})


# 待收货
def payed(request):

    if request.method == 'GET':
        user = request.user
        user_orders_goods = order_goods(user, 1)
        return render(request, 'order/order_list_payed.html', {'user_orders_goods': user_orders_goods})


# 获取用户的OrderGoodsModel信息
def order_goods(user, status):
    orders = OrderModel.objects.filter(user=user, o_status=status)
    user_orders_goods = []
    for order in orders:
        orders_goods = OrderGoodsModel.objects.filter(order=order)
        for order_goods in orders_goods:
            user_orders_goods.append(order_goods)
    return user_orders_goods

# 获取所有已选择商品的总价
def total_price(user):
    all_select = CartModel.objects.filter(user=user, is_select=True)
    total_price = 0
    for selected in all_select:
        total_price += selected.goods.price * selected.c_num
        total_price = round(total_price, 2)
    return total_price


# 生成随机订单编号
def orderNumber():
    s = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    o_number = ''
    for x in range(10):
        o_number += random.choice(s)
    return o_number


# 判断购物车是否全选
def is_select_all(user):
    carts = CartModel.objects.filter(user=user, is_select=False)
    if carts:
        is_select_all = False
    else:
        is_select_all = True
    return is_select_all
