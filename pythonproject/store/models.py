from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

#顧客模型建立
class Customer(models.Model):
    #每個使用者(User)都只能對應到一個客戶(Customer)
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True,blank = True)
    #顧客的姓名
    name = models.CharField(max_length = 200,null = True)
    #顧客的email
    email = models.CharField(max_length = 200,null = True)

    #指定以顧客姓名作為標題呈現
    def __str__(self):
        return self.name

#商品類別模型
class Category(models.Model):
    #類別名稱
    name = models.CharField(max_length=200, null = True)
    #用於生成便於閱讀的網址形式，有助於追蹤並對應特定網址
    slug = models.SlugField(max_length=200, unique=True, null = True)  # 用於在 URL 中識別類別

    #根據類別名稱排序
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name

    #此定義代表每個類別都有其對應的url，以確保類別與商品不會對應錯誤
    def get_absolute_url(self):
        return reverse('store_by_category', args=[self.slug])

#商品模型
class Product(models.Model):
    #商品名稱
    name = models.CharField(max_length=200,null = True)
    #商品價格
    price = models.DecimalField(max_digits = 100, decimal_places = 0)
    #商品圖片
    image = models.ImageField(null = True, blank = True)
    #商品類別(商品與類別建立多對多關聯，一個商品可有多個類別)
    category = models.ManyToManyField(Category, related_name='products', blank=True)
    #商品單位 (例如：斤、條、個、片)
    unit = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.name

    #從self.image中取得圖片的url，若沒有該內容則返回空字串
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

#商品訂單模型
class Order(models.Model):
    #顧客與商品訂單建立關聯，一位顧客可以有多個訂單
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank = True)
    #訂單成立時間
    date_ordered = models.DateTimeField(auto_now_add = True)
    #訂單是否完成的標記
    complete = models.BooleanField(default = False)
    #交易編號
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return str(self.id)
   # @property
    #def shipping(self):
       # orderitems = self.orderitem_set.all()
       # return orderitems

    #計算訂單內所有商品的總金額
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    #計算訂單內所有商品的總數量
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

#訂單內的商品模型(訂單中有的商品)
class OrderItem(models.Model):
    #訂單中的商品
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null=True, blank = True)
    #訂單
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True)
    #訂購的商品數量
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    #訂購時間
    date_added = models.DateTimeField(auto_now_add = True)

    #計算該商品的總金額
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


#class ShippingAddress(models.Model):
   # customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null=True, blank = True)
    #order = models.ForeignKey(Order, on_delete = models.SET_NULL, null=True, blank = True)
  #  name = models.CharField(max_length=200,null = True)
   # address = models.CharField(max_length=200,null = True)
   # state = models.CharField(max_length=200,null = True)
   # zipcode = models.CharField(max_length=200,null = True)
   # date_added = models.DateTimeField(auto_now_add = True)



