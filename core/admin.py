



# # Register your models here.
from django.contrib import admin
from core.models import Category, Product, Vendor, CartItemOrders, CartOrders, Wishlist, Address, ProductImages, Product_Review


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['user', 'title', 'product_image', 'category', 'price', 'featured', 'product_status', ]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']


class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class CartOrdersAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['id', 'user', 'price', 'paid_status', 'order_date', 'product_status']


class CartItemOrdersAdmin(admin.ModelAdmin):
    
    list_display = ['user', 'order_image' ,'order_user', 'price', 'item', 'quantity', 'product_status', 'invoice_no', 'total_price']

    def order_user(self, obj):
        return obj.order.user
    order_user.short_description = 'User'


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'Product', 'rating', 'date']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'Product', 'date']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'mobile', 'alternate_mobile', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartItemOrders, CartItemOrdersAdmin)
admin.site.register(CartOrders, CartOrdersAdmin)
admin.site.register(Product_Review, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)