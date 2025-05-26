from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauth.models import User
from  taggit.managers import TaggableManager

STATUS_CHOICE = [
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
]

STATUS = [
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("rejected", "Rejected"),
    ("published", "Published"),
]

RATING = [
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
]

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='cat', alphabet="abcdefghi12345")
    title = models.CharField(max_length=100, default="Clothes")
    image = models.ImageField(upload_to="Category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" /> ' % (self.image.url))
    
    def __str__(self):
        return self.title

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='ven', alphabet="abcdefghi12345")
    title = models.CharField(max_length=100, default="Stunning Abaya")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    cover_image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    desc = models.TextField(null=True, blank=True, default="Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nam beatae consectetur, atque inventore aliquam adipisci perspiciatis nostrum qui consequatur praesentium?")

    address = models.CharField(max_length=100, default="123, London Street")
    contact = models.CharField(max_length=100, default="+244533112")
    chat_resp_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    shipping_time = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date= models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vendors"

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, prefix='prd', alphabet="abcdefghi12345")
    title = models.CharField(max_length=100, default="Stunning Abaya")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    desc = models.TextField(null=True, blank=True, default="Lorem ipsum dolor sit, amet consectetur adipisicing elit. Nam beatae consectetur, atque inventore aliquam adipisci perspiciatis nostrum qui consequatur praesentium?")
    vendor=  models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name="vendor")

    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")

    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=2.99)
    get_percentage=models.DecimalField(max_digits=10, decimal_places=0, default=100)

    specifications = models.TextField(null=True, blank=True)
    # type = models.TextField(max_length=100, null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    tags= TaggableManager(blank= True)

    product_status = models.CharField(choices=STATUS, max_length=100, default="process")
    
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet="abcdefghi12345")

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" /> ' % (self.image.url))
    
    def __str__(self):
        return self.title

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product_images", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"

class CartOrders(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)

    product_status = models.CharField(choices=STATUS_CHOICE, max_length=100, default="process")

    class Meta:
        verbose_name_plural = "Cart Orders"

class CartItemOrders(models.Model):
    invoice_no= models.CharField(max_length=100)
    order = models.ForeignKey(CartOrders, on_delete=models.CASCADE)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=255)  # Fixed missing max_length
    quantity = models.IntegerField(default=0)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=1.99)

    class Meta:
        verbose_name_plural = "Cart Items"

    def order_image(self):
        return mark_safe('<img src = "/media/%s" width="50", hieght= "50" />' % (self.image) )

######################## Product Review , Wishlist, Address ###################################
 
class Product_Review(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    Product=models.ForeignKey(Product, on_delete=models.SET_NULL, null= True, related_name="review")
    review=models.TextField(max_length=499)
    rating=models.IntegerField(choices=RATING, default=None)
    date= models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Product Reviews"

    def __str__(self):
        return self.Product.title
    
    def __str__(self):
        return str(self.rating)

    
class Wishlist(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    Product=models.ForeignKey(Product, on_delete=models.SET_NULL, null= True)
    date= models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Wishlists"

    def __str__(self):
        return self.Product.title

class Adress(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null= True)
    address= models.CharField(max_length=400, null=True),
    status=models.BooleanField(default=True)

    class Meta:
        verbose_name_plural="Adresses"



# Create your models here.