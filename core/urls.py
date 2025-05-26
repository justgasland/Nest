from django.urls import path
from .views import home, productlist, product_details_view, category_lists_view, category_product_list_view, vendor_lists_view, vendor_details_view, tag_list, Review_form
from .views import search_view, filter_products
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
]
