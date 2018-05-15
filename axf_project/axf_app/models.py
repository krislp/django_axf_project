from django.db import models


# Create your models here.
class Main(models.Model):

    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # 通用id

    class Meta:
        # 抽象类
        abstract = True


class MainWheel(Main):
    # 轮播banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


# 主要商品展示表
class MainShow(Main):
    categoryid = models.CharField(max_length=16)
    brandname = models.CharField(max_length=100)

    childcid1 = models.CharField(max_length=16, null=True)
    productid1 = models.CharField(max_length=16, null=True)
    img1 = models.CharField(max_length=200)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)


    childcid2 = models.CharField(max_length=16, null=True)
    productid2 = models.CharField(max_length=16, null=True)
    img2 = models.CharField(max_length=200)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)


    childcid3 = models.CharField(max_length=16, default=True)
    productid3 = models.CharField(max_length=16, null=True)
    img3 = models.CharField(max_length=200)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


# 闪购 -- 左侧类型表
class FoodType(models.Model):
    # 分类id
    typeid = models.CharField(max_length=16)
    # 类型名称
    typename = models.CharField(max_length=100)
    # 类型
    childtypenames = models.CharField(max_length=200)
    # 排序
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


# 商品表
class Goods(models.Model):
    # 商品编号
    productid = models.CharField(max_length=16)
    # 商品图片
    productimg = models.CharField(max_length=200)
    # 商品名称
    productname = models.CharField(max_length=100)
    # 商品规范名称
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    # 规格
    specifics = models.CharField(max_length=100)
    # 折后价
    price = models.FloatField(default=0)
    # 原价
    marketprice = models.FloatField(default=1)
    # 分类id
    categoryid = models.CharField(max_length=16)
    # 子分类id
    childcid = models.CharField(max_length=16)
    # 子分类名称
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    # 排序
    storenums = models.IntegerField(default=1)
    # 销量排序
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


# 用户信息表
class UserModel(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    # False 女 True 男
    sex = models.BooleanField(default=False)
    # 头像
    icon = models.ImageField(upload_to='icons')
    # 是否删除
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'


# 用户ticket表
class UserTicket(models.Model):
    user = models.ForeignKey(UserModel)
    ticket = models.CharField(max_length=255)
    out_time = models.FloatField()

    class Meta:
        db_table = 'axf_user_ticket'


# 购物车
class CartModel(models.Model):
    '''
    user 关联用户
    goods 关联商品
    c_num 商品数量
    is_select 是否选择
    '''
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


# 订单表
class OrderModel(models.Model):
    '''
    user 用户
    o_number 订单编号
    o_status 订单状态 0 下单，未付款 1 已付款，未发货
    o_create 订单创建时间
    '''
    user = models.ForeignKey(UserModel)
    o_number = models.CharField(max_length=64)
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'


# 订单商品关联表
class OrderGoodsModel(models.Model):
    '''
    goods 关联的商品
    order 关联的订单
    goods_num 商品的个数
    '''
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    goods_num = models.IntegerField(default=1)

    class Meta:
         db_table = 'axf_order_goods'