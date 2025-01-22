import datetime
import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import *
from .utils import cartData, cookieCart, guestOrder

# Create your views here.

#商品頁面，顯示所有商品或特定分類的商品
def store(request, category_slug=None):
    #獲取購物車數據
    data = cartData(request)
    cartItems = data['cartItems']

    #取得所有分類與商品
    categories = Category.objects.all()
    category = None
    products = Product.objects.all()

    #如果有分類slug，會篩選特定分類的商品
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = Product.objects.filter(category=category)

    context = {'products':products, 'cartItems':cartItems,
               'categories': categories, 'category': category}
    return render(request, 'store/store.html', context)

#購物車頁面，顯示顧客(使用者)已加入購物車的商品
def cart(request):
    #獲取購物車數據
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items':items,'order':order,
               'cartItems':cartItems}
    return render(request, 'store/cart.html',
                   context)

# 結帳頁面，顯示購物車商品的訂單資訊
def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items':items,'order':order,
               'cartItems':cartItems}
    return render(request, 'store/checkout.html',
                  context)

#更新購物車的商品數量與狀態
def updateItem(request):

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    #獲取當前的用戶和商品資訊
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer= customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product = product)

    #如果按增加按紐，商品數量將加1/按減少按紐，商品數量將減1
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    #當商品數量小於0，訂單會整筆刪除
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)

#處理訂單付款，並送出訂單
def processOrder(request):
    #生成唯一的交易ID
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    #如果使用者已經登入，則以該使用者為訂單的對應顧客
    #註：此處的登入不是網站的登入，而是後台管理的登入
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete=False)

    #如果未登入，則以訪客身分下單
    else:
        customer, order = guestOrder(request, data)

    #獲取總金額並設置交易ID
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    #驗證總金額是否一致，若一致則完成訂單
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    return JsonResponse('Payment submitted..', safe=False)

