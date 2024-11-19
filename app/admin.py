from django.contrib import admin
from .models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id','title','selling_price','discounted_price','category','product_image']
    
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','zip_code']

@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(Payment)
class AdminPayment(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class AdminOrderPlaced(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']

@admin.register(Wishlist)
class AdminWishlist(admin.ModelAdmin):
    list_display = ['id','user','product']