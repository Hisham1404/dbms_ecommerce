from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name_plural = 'categories'

class Customer(models.Model):
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    # password = models.CharField(max_length=100)


    def __str__(self):
        if self.user:
            return self.user.username
        else:
            return "No User Assigned"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank =True, null=True)
    image = models.ImageField(upload_to = 'uploads/product/')
    is_sale = models.BooleanField(default= True)
    sale_price = models.DecimalField(default=0,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name
    
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(default=timezone.now, blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        
        
        return shipping
    
    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.product.price * item.quantity for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total



class OrderItem(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # address = models.CharField(max_length=100,default='',blank=True)
    # phone = models.CharField(max_length=50,default='',blank=True)
    date_added = models.DateField(default=datetime.datetime.today)
    # status = models.BooleanField(default=False)


    def __str__(self):
        return self.product.name
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.first_name
    



    