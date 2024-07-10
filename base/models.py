from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import models


# Create your models here.
class Book(models.Model):
  name=models.CharField(max_length=200,null=False)
  url=models.CharField(max_length=2000,null=True)
  description=models.CharField(max_length=500,null=False)
  author=models.CharField(max_length=200)
  genre=models.CharField(max_length=200)
  price=models.DecimalField(max_digits=6, decimal_places=2,default=1.0,null=False, validators=[MinValueValidator(Decimal('0.01'))])
  added=models.DateTimeField(auto_now_add=True)
  is_featured=models.BooleanField(default=False)
  discount=models.DecimalField(max_digits=6, decimal_places=2,null=True,default=0.0, validators=[MinValueValidator(Decimal('0.00'))])

  def __str__(self):
    return self.name
  
  @property
  def price_after_discount(self):
    return self.price - self.discount
  
class Genre(models.Model):
  genre=models.CharField(max_length=200)

  def __str__(self):
    return self.genre
  
class Order(models.Model):
  customer=models.ForeignKey(User,on_delete=models.SET_NULL, blank=True,null=True)
  date_ordered= models.DateTimeField(auto_now_add=True)
  complete=models.BooleanField(default=False,null=True,blank=False)
  transaction_id=models.CharField(max_length=200,null=True)

  def __str__(self):
    return str(self.id)
  
  @property
  def total_price(self):
    items = OrderItem.objects.filter(order=self) or []
    return sum(item.total_price for item in items)
  
  @property
  def shipping_address(self):
    return ShippingAddress.objects.get(order=self)
  
  @property
  def items_count(self):
    items = OrderItem.objects.filter(order=self) or []
    return len(items)

class OrderItem(models.Model):
  book=models.ForeignKey(Book,on_delete=models.SET_NULL, blank=True,null=True)
  order=models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
  quantity=models.IntegerField(default=0, null=True, blank=True)
  date_added=models.DateTimeField(auto_now_add=True)

  @property
  def total_price(self):
    return self.book.price * self.quantity


class ShippingAddress(models.Model):
  customer=models.ForeignKey(User,on_delete=models.SET_NULL, blank=True,null=True)
  order=models.ForeignKey(Order, on_delete=models.SET_NULL,blank=True,null=True)
  address=models.CharField(max_length=200, null=True)
  city=models.CharField(max_length=200, null=True)
  state=models.CharField(max_length=200, null=True)
  zipcode=models.CharField(max_length=200, null=True)
  date_added=models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.address
  

  






  