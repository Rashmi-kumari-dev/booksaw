from django.db import models


# Create your models here.
class Book(models.Model):
  name=models.CharField(max_length=200,null=False)
  url=models.CharField(max_length=2000,null=True)
  description=models.CharField(max_length=500,null=False)
  author=models.CharField(max_length=200)
  genre=models.CharField(max_length=200)
  price=models.CharField(max_length=50,null=False)
  added=models.DateTimeField(auto_now_add=True)
  is_featured=models.BooleanField(default=False)

  def __str__(self):
    return self.name
  
class Genre(models.Model):
  genre=models.CharField(max_length=200)

  def __str__(self):
    return self.genre



  