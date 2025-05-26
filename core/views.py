from django.shortcuts import render
from core.models import Product, CartItemOrders, CartOrders, Category, ProductImages, Product_Review, Wishlist, Vendor
from django.db.models import Count, Avg
from taggit.models import Tag
from django.shortcuts import get_object_or_404
from core.forms import ProductReviewForms
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.template.loader import render_to_string 




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

# Create your views here.

