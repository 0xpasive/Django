from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(null=True, blank=True, max_length=100)
    joined_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.full_name

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True) #slug is a URL friendly version of the title



    def __str__(self):
        return self.title

class Product(models.Model):
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #on delete means if the category is deleted, the product will also be deleted
    originalprice = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images')

    def __str__(self):
        return self.name

   
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    cart_id = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "Cart: " + self.cart_id
    
class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return "Cart: " + self.cart.cart_id + " CartProduct: " + self.product.name
    
ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    
    ('Order Processing', 'Order Processing'),
    ('Order Shipped', 'Order Shipped'),
    ('Order Delivered', 'Order Delivered'),
    ('Order Cancelled', 'Order Cancelled'),
)
class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=ORDER_STATUS, default='Order Processing')
    
    def __str__(self):
        return "Order: " + self.order_id
    
