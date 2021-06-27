from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from .models import *

# Register your models here.
#admin.site.register(Customer)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']
    list_filter =['name']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    readonly_fields=['photo_tag'] #it will give preview image inside the object form in admin
    save_on_top = True
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category','photo_tag', 'product_image' ]
    list_filter =['category']
    def photo_tag(self,obj):
        return format_html(f'<img src="/media/{obj.product_image}" style="height:30px;widhth:30px;>')

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    list_filter =['user']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','customer_info', 'product','product_info', 'quantity', 'ordered_date', 'status']
    list_filter=['ordered_date']
    def customer_info(self, obj):
        #link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html(f'<a href ="/admin/app/customer/{obj.customer.pk}/change/">{obj.customer.name}</a>' )
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href ="{}">{}</a>', link, obj.product.title)