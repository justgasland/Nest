from django.shortcuts import render
from core.models import Product, CartItemOrders, CartOrders, Category, ProductImages, Product_Review, Wishlist, Vendor, Address
from django.db.models import Count, Avg
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from core.forms import ProductReviewForms
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string 
from django.shortcuts import redirect
from django.contrib import messages




def home(request):
    product= Product.objects.all()


    context={
        'product': product
    }
    
    return render(request, 'index.html', context)

def productlist(request):
    product= Product.objects.all()

    context={
        'products': product
    }
    
    return render(request, 'product-list.html', context)



def category_lists_view(request,):
    categories= Category.objects.all()

    context={

        'categories': categories
    }
    
    return render(request, 'category-list.html', context)

def category_product_list_view(request, cid ):
    categories= Category.objects.get(cid=cid)
    products= Product.objects.filter(product_status= "published", category= categories)

    context={

        'categories': categories,
        'products': products
    }
    
    return render(request, 'category-product-list.html', context)

def vendor_lists_view(request,):
    vendors= Vendor.objects.all()

    context={

        'vendors': vendors
    }
    
    return render(request, 'vendors-list.html', context)

def vendor_details_view(request, vid):
    vendors = Vendor.objects.get(vid=vid)
    products= Product.objects.filter(product_status= "published", vendor= vendors)

    context={

        'vendors': vendors,
        'products': products,
    }
    
    return render(request, 'vendor-details-2.html', context)

def product_details_view(request, pid):
    products= Product.objects.get(pid=pid)
    vendors=products.vendor
    product=Product.objects.filter(category=products.category).exclude(pid=pid)

    # Getting Review
    review=Product_Review.objects.filter(Product=products).order_by("-date")

    # Average Rating
    average_rating=Product_Review.objects.filter(Product=products).aggregate(rating=Avg('rating'))

    # Product Review Form
    review_form=ProductReviewForms()

    # make_review= True
    # if request.user.is_authenticated:
    #     user_review_count = Product_Review.objects.filter(user=request.user, Product=products).count()
    #     if user_review_count > 0:
    #         make_review= False



    context={

        'products': products,
        'vendors': vendors,
        'review': review, 
        # 'make_review': make_review,
        'p': product,
        'avg_rating': average_rating,
        'reviewform':review_form
    }
    
    return render(request, 'product-details.html', context)



def tag_list(request, tag_slug=None):
    tag = None
    products = Product.objects.filter(product_status="published").order_by("-id")

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        'products': products,
        'tag': tag
    }
    return render(request, 'tagslist.html', context)


def Review_form(request, pid):
    products=Product.objects.get(pid=pid)
    user= request.user

    review=Product_Review.objects.create(
        user=user,
        Product=products,
        review= request.POST['review'],
        rating= request.POST['rating'],
    )
    
    
    
    average_review = Product_Review.objects.filter(Product=products).aggregate(rating=Avg('rating'))
    
    
    context={
        'user': user.username,
        
        'review':  request.POST.get('review'),
        'rating': request.POST.get('rating'),

    }

    return JsonResponse(
        {'bool': True,
        'context': context,
        'average_review': average_review,
        }
    )

def search_view(request) :
    query= request.GET.get('q')
    # products=Product.objects.filter(title__icontains=query, desc__icontains=query).order_by("date")
    products = Product.objects.filter(
        Q(title__icontains=query) | Q(desc__icontains=query)
        ).order_by("date")
    
    context={
        "products":products,
        "query": query,
    }
    
    
    return render(request, "search.html", context)

def filter_products(request):

    categories= request.GET.getlist("category[]")
    vendors= request.GET.getlist("vendor[]")

    
    # min_price = request.GET.get["min_price"]
    # max_price = request.GET.get["max_price"]
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")


    products= Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)
    
    if len(categories) > 0:
        products = Product.objects.filter(category__in=categories).distinct()
    if len(vendors)> 0:
        products = Product.objects.filter(vendor__in=vendors).distinct()
    
    data=render_to_string("core/async/filter_products.html", {'products': products,})
    return JsonResponse({'data': data}) 

def add_to_cart(request):
    cart_product={}
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],  
        'price': float(request.GET['price']),
        'qty': int(request.GET['qty']),
        'image': request.GET['image'],
        'pid': request.GET['pid'],

    }
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data=request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty']  = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product


    return JsonResponse({"data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for id, item in request.session['cart_data_obj'].items():
            item['qty'] = int(item['qty'])
            cart_total_amount += int(item['qty']) * float(item['price'])

        return render(request, 'core/cart.html', {"cart_data": request.session['cart_data_obj'], "totalcartitems": len(request.session['cart_data_obj']) , "cart_total_amount": cart_total_amount})
    else:
        messages.warning(request, "Your cart is empty!")  
        return redirect('home')

def delete_from_cart(request):  
    print("Session cart_data_obj:", request.session.get('cart_data_obj', {}))
    product_pid = request.GET.get('id')
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        keys_to_delete = [key for key, item in cart_data.items() if item['pid'] == product_pid]
        for key in keys_to_delete:
            del cart_data[key]
        
        
        request.session['cart_data_obj'] = cart_data
        request.session.modified = True
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    

    

    context= render_to_string("core/async/cart_list.html", {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),  "cart_total_amount": cart_total_amount}  )
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])}) 



def update_from_cart(request):  
    print("Session cart_data_obj:", request.session.get('cart_data_obj', {}))
    product_pid = request.GET.get('id')
    product_qty = request.GET.get('qty')
    
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']
        updated = False
        for key, item in cart_data.items():
            if item['pid'] == product_pid:
                cart_data[key]['qty'] = int(product_qty)
                updated = True
                print(f"Updated item {key} with PID {product_pid} to quantity {product_qty}")
        
        
        cart_data[str(request.GET['id'])]['qty']  = int(product_qty[str(request.GET['id'])]['qty'])
        
        request.session['cart_data_obj'] = cart_data
        request.session.modified = True
    
    
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    context= render_to_string("core/async/cart_list.html", {'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),  "cart_total_amount": cart_total_amount}  )
    return JsonResponse({'data': context, 'totalcartitems': len(request.session['cart_data_obj'])}) 


from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required

@login_required
# def checkout_view(request):
    
#     cart_toal_amount = 0
#     total_amount=0

#     if 'cart_data_obj' in request.session:
#         for id, item in request.session['cart_data_obj'].items():
#             # item['qty'] = int(item['qty'])
#             total_amount += int(item['qty']) * float(item['price'])

#             order = CartItemOrders.objects.create(
#                 user=request.user,
#                 price=total_amount
#             )
        
#         for id, item in request.session['cart_data_obj'].items():
#             cart_toal_amount += int(item['qty']) * float(item['price'])
    
#             cart_orders = CartOrders.objects.create(
#                 order= order,
#                 invoice_no= "INVOICE-ID " + str(order.id),
#                 item=item['title'],
#                 image=item['image'],
#                 qty=item['qty'],
#                 price=item['price'],
#                 total= float(item['qty']) * float(item['price']),

#             )
    
    
    
#     host= request.get_host()
#     paypal_dict= {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': cart_toal_amount,
#         'item_name': 'Order-Item-No-1 ' + str(order.id),
#         'invoice': 'INV-001 ' + str(order.id),
#         'currency_code': 'USD',
#         'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
#         'return_url': 'http://{}{}'.format(host, reverse('payment-completed')),
#         'cancel_url': 'http://{}{}'.format(host, reverse('payment-failed')),
#     }

#     paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

#     cart_total_amount = 0
#     if 'cart_data_obj' in request.session:
#         for id , item in request.session['cart_data_obj'].items():
#             cart_total_amount += int(item['qty']) * float(item['price'])
    
#     return render(request, 'core/checkout.html' ,{'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),  "cart_total_amount": cart_total_amount, "paypal_payment_button":paypal_payment_button })
    
@login_required
def checkout_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' not in request.session:
        messages.warning(request, "Your cart is empty!")
        return redirect('home')

    # Calculate total amount
    for item in request.session['cart_data_obj'].values():
        cart_total_amount += int(item['qty']) * float(item['price'])

    # Step 1: Create the master order
    order = CartOrders.objects.create(
        user=request.user,
        price=cart_total_amount
    )

    # Step 2: Create each item linked to the order
    for item in request.session['cart_data_obj'].values():
        CartItemOrders.objects.create(
            user=request.user,
            order=order,
            invoice_no="INV-" + str(order.id),
            product_status="processing",
            item=item['title'],
            image=item['image'],
            quantity=item['qty'],
            price=item['price'],
            total_price=float(item['qty']) * float(item['price'])
        )

    # Step 3: Setup PayPal
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amount,
        'item_name': 'Order-Item-No-1 ' + str(order.id),
        'invoice': 'INV-001 ' + str(order.id),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}{reverse("payment-completed")}',
        'cancel_url': f'http://{host}{reverse("payment-failed")}',
    }

    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    return render(
        request,
        'core/checkout.html',
        {
            'cart_data': request.session['cart_data_obj'],
            'totalcartitems': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount,
            'paypal_payment_button': paypal_payment_button
        }
    )


def payment_completed(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for id , item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    return render(request, 'core/paymentcompleted.html' ,{'cart_data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']),  "cart_total_amount": cart_total_amount})
    

def payment_failed(request):
    return render(request, 'core/paymentfailed.html')


@login_required
def customer_dashboard(request):
    orders = CartOrders.objects.filter(user=request.user)
    address = Address.objects.filter(user=request.user)
    
    if request.method == "POST":
        address= request.POST['address']
        mobile= request.POST['mobile']
        new_Address= Address.objects.create(user=request.user, address=address, mobile=mobile)
        messages.success(request, "address saved")
        return redirect ('customer-dashboard')

    context = {
        'orders': orders,
        'address': address
    }


    return render(request, 'core/customer-dashboard.html', context)




def order_detail(request, id):
    order = CartOrders.objects.get(id=id, user=request.user)
    
    order_items = CartItemOrders.objects.filter(order=order)
    
    
    context = {
        
        'order_items': order_items
    }
    
    
    return render(request, 'core/order-detail.html', context)