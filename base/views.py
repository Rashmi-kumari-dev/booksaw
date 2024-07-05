from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book, Genre
import math



def home(request):
  books=Book.objects.filter(is_featured=True)
  discountedBooks = Book.objects.filter(discount__gt=0)
  booksByGenre = {
    'romance': Book.objects.filter(genre__icontains='Romance'),
    'technology': Book.objects.filter(genre__icontains='Technology'),
    'fantasy': Book.objects.filter(genre__icontains='Fantasy'),
    'adventure': Book.objects.filter(genre__icontains='Adventure'),
    'non_fiction': Book.objects.filter(genre__icontains='Non-fiction'),
  }
  coverBooks = Book.objects.all()[:5]
  context= {
    'books':books, 
    'discountedBooks': discountedBooks,
    'booksByGenre':booksByGenre,
    'coverBooks': coverBooks
  }
  return render(request,'base/home.html',context)

def book(request, pk):
  book=Book.objects.get(id=pk)
  context={'book':book}
  return render(request,'base/book.html',context)

def loginPage(request):
  if request.method=='POST':
    email=request.POST.get('email')
    password=request.POST.get('password')
    try:
      user=User.objects.get(email=email)
    except:
      messages.error(request, "User does not exits.")
    user=authenticate(request,email=email,password=password)

    if user is not None:
      login(request,user)
      return redirect('home')
    else:
       messages.error(request, "Username or Password  does not match.")

  context={}
  return render(request, 'base/login.html',context)

def logoutUser(request):
  logout(request)
  return redirect ('/home')


def books(request):
  books=Book.objects.all()
  context={'books':books}
  return render(request,'base/books.html',context)

def offer(request):
  books=Book.objects.filter(discount=False)
  context={'books':books}
  return render(request,'base/home.html',context)


def vision(request):
  return render(request,'base/vision.html')


