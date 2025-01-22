import json
from . models import *

#處理未登入之使用者的訂單資訊
def cookieCart(request):

    #從Cookies中提取購物車的訂單資訊
    try:
        cart = json.loads(request.COOKIES['cart'])

    except:
        cart = {}

    print('Cart:', cart)
    items = []
    order ={'get_cart_total':0, 'get_cart_items':0}

    #初始化購物車商品的總數量為0
    cartItems = order['get_cart_items']


    for i in cart:
        try:
            #累加購物車中的商品數量
            cartItems += cart[i]['quantity']

            #計算每個商品的總價
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            #更新訂單的總金額與總數量
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            #將商品資訊儲存為字典
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            #將新增的商品新增至items中
            items.append(item)

        except:
            pass

    return {'items':items, 'order':order, 'cartItems':cartItems}

#根據使用者登入狀態獲取購物車資訊
def cartData(request):

    #使用者有登入，可直接從後台獲取顧客、訂單等資訊
    if request.user.is_authenticated:
        customer =request.user.customer
        order, created = Order.objects.get_or_create(customer= customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    #使用者未登入，使用cookieCart獲取購物車資訊
    else:
        cookieData = cookieCart(request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    return {'items':items,'order':order,'cartItems':cartItems}

#處理訪客的訂單資訊(訪客就是未登入的使用者)
def guestOrder(request, data):

    #此處為提示使用者未登入的訊息
    print('User is not logged in..')
    print('COOKIES:', request.COOKIES)

    #從表單中獲取使用者的姓名與email
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    #建立或獲取使用者資料
    user, exist = User.objects.get_or_create(username=name, email=email)

    #建立或獲取顧客資料
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.user=user
    customer.save()

    #建立新訂單
    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    #將購物車的每個商品加入至訂單中
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem  = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order