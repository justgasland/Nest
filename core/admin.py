# from django.contrib import admin
# from core.models import Category, Product, Vendor, CartItemOrders, CartOrders, Wishlist, Adress, ProductImages, Product_Review


# class ProductImagesAdmin(admin.TabularInline):
#     model=ProductImages

# class ProductAdmin(admin.ModelAdmin):
#     inlines= [ProductImagesAdmin]
#     list_display=['user', 'title', 'product_image', 'price', 'featured', 'product_status']

# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['title', 'category_image']

# class VendorAdmin(admin.ModelAdmin):
#     list_display=['title', 'Vendor_image']

# class CartOrdersAdmin(admin.ModelAdmin):
#     list_display=['user', 'price', 'paid_status', 'order_date', 'product_status']

# class CartItemOrdersAdmin(admin.ModelAdmin):
#     list_display=['user', 'price', 'item', 'quantity' ,'product_status', 'invoice_no', 'total_price']
    
# class ProductReviewAdmin(admin.ModelAdmin):
#     list_display=['user','review', 'product', 'rating', 'date']

# class WishlistAdmin(admin.ModelAdmin):
#     list_display=['user', 'product', 'date']

# class AdressAdmin(admin.ModelAdmin):
#     list_display=['user', 'product', 'date']

# admin.site.register(Product, ProductAdmin)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Vendor, VendorAdmin)
# admin.site.register(CartItemOrders, CartItemOrdersAdmin)
# admin.site.register(CartOrders, CartOrdersAdmin)
# admin.site.register(Product_Review, ProductReviewAdmin)
# admin.site.register(Wishlist, WishlistAdmin)
# admin.site.register(Adress, AdressAdmin)




# # Register your models here.
from django.contrib import admin
from core.models import Category, Product, Vendor, CartItemOrders, CartOrders, Wishlist, Adress, ProductImages, Product_Review


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
    list_display = ['order', 'price', 'paid_status', 'order_date', 'product_status']


class CartItemOrdersAdmin(admin.ModelAdmin):
    list_display = ['order_user', 'price', 'item', 'quantity', 'product_status', 'invoice_no', 'total_price']

    def order_user(self, obj):
        return obj.order.order
    order_user.short_description = 'User'


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'Product', 'rating', 'date']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'Product', 'date']


class AdressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartItemOrders, CartItemOrdersAdmin)
admin.site.register(CartOrders, CartOrdersAdmin)
admin.site.register(Product_Review, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Adress, AdressAdmin)