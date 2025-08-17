from django.urls import path
from .views import home, productlist, product_details_view, category_lists_view, category_product_list_view, vendor_lists_view, vendor_details_view, tag_list, Review_form
from .views import search_view, filter_products, add_to_cart , cart_view, delete_from_cart, update_from_cart, checkout_view
from django.urls import include

from .views import payment_completed, payment_failed, customer_dashboard, order_detail

urlpatterns = [
    # product
    path('', home, name='home'),
    path('products/', productlist, name='products'),
    path('products/<pid>', product_details_view, name='product-details'),
     
    # Category
    path('category/', category_lists_view, name='category'),
    path('category/<cid>', category_product_list_view, name='category-product-list'),

    # Vendor
    path('vendor/', vendor_lists_view, name='vendor'),
    path('vendor/<vid>', vendor_details_view, name='vendor-details'),
    

    # Tags
    path('products/tag/<tag_slug>/', tag_list, name='tags'),

    # Add Review
    path('reviewform/<pid>', Review_form, name='reviewforms'),

    # Search
    path('search/', search_view, name='search'),
    path( 'filter-products/' , filter_products, name='filter_products'),

    # add to cart
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    
    # Viewing Cart 
    path('cart/', cart_view, name='cart_view'),

    # delete from cart
    path('delete-from-cart/', delete_from_cart, name='delete_from_cart'),

    # Update Cart
    path('update-cart/', update_from_cart, name='update_cart'),

    # Checkout
    path('checkout/', checkout_view, name='checkout_view'),

    # Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    # Payment Completed
    path('payment-completed/', payment_completed, name='payment-completed'),

    # payment failed
    path('payment-failed/', payment_failed, name='payment-failed'),

    # Customer Dashboard
    path('customer-dashboard/', customer_dashboard, name='customer-dashboard'),

    # Order Detail
    path('order-detail/<int:id>/', order_detail, name='order-detail'),
]
