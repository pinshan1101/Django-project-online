from django.urls import path

from . import views


urlpatterns  = [
    #商店主頁的網址
    path('',views.store, name = "store"),

    #根據特定分類顯示商品列表，使用 slug 作為分類識別符
    path('store/category/<slug:category_slug>/', views.store, name='store_by_category'),

    #購物車頁面，顯示顧客(使用者)已加入購物車的商品
    path('cart/',views.cart, name = "cart"),

    #結帳頁面，處理顧客的結帳流程
    path('checkout/',views.checkout, name = "checkout"),

    #更新購物車中的商品數量、金額等資訊
    path('update_item/',views.updateItem, name = "update_item"),

    #處理訂單流程，包含付款與送出訂單
    path('processOrder/',views.processOrder, name = "process_order"),

]