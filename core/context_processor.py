from core.models import Product, CartItemOrders, CartOrders, Category, ProductImages, Product_Review, Wishlist, Vendor
from django.db.models import Count, Avg, Min, Max


def default(request):
    category= Category.objects.all()
    product= Product.objects.all()
    vendor= Vendor.objects.all()

    min_max_price=Product.objects.aggregate(Min('price'), Max('price'))
    
    return{
        'category': category,
        'product': product,
        'vendor': vendor,
        'min_price': min_max_price,
    }
    