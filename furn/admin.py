from django.contrib import admin
from . models import Blog, Product, Contact, OrderItem, Orders, Address, Payment
# Register your models here.




@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'date']
    list_filter = [ 'title', 'date']
    search_fields = ['user__username', 'title', 'date']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['name', 'price']
    search_fields = ['name', 'price']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'message']
    search_fields = ['first_name','email' ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    search_fields = ['product']

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['user','ref_number','address','ordered', 'delivered', 'order_date']
    list_filter = ['ordered', 'delivered', 'order_date']
    list_display_links = ['address', 'user']
    search_fields = ['ref_number', 'order_date', 'address__address']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['country', 'phone_number', 'email']
    search_fields = ['country', 'phone_number', 'email']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['user', 'amount']
    search_fields=['user__username', 'amount', 'stripe_charge_id']
