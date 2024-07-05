from django.shortcuts import render
from .models import Book, Genre
import math



def home(request):
  # q=request.Get.get('q') if request.GET.get('q')!=None else ''
  # books=Book.objects.filter(genres__name__contains=q)
  books=Book.objects.filter(is_featured=True)
  context={'books':books}
  return render(request,'base/home.html',context)

def book(request, pk):
  book=Book.objects.get(id=pk)
  context={'book':book}
  return render(request,'base/book.html',context)

def login(request):
  return render(request, 'base/login.html')

def books(request):
  books=Book.objects.all()
  context={'books':books}
  return render(request,'base/books.html',context)

