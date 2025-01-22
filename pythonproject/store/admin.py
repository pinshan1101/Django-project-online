import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Sum
from django.db.models.functions import TruncDay

from .models import *

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "order","quantity","date_added")
    ordering = ("-date_added",)

    def changelist_view(self, request, extra_context=None):
        chart_data = (
            OrderItem.objects.values("product__name")  # 商品名稱
            .annotate(y=Sum("quantity"))  # 購買商品數量加總
            .order_by("product__name")  # Sort by product name
        )

        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        return super().changelist_view(request, extra_context=extra_context)




admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem, ItemAdmin)
admin.site.register(Category)
#admin.site.register(ShippingAddress)
