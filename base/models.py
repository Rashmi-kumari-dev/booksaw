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



  