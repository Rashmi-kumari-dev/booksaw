from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book, Genre, Order, OrderItem, ShippingAddress
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import uuid
from .quote_generator import generate_quote

def getCartItemCount(request):
  cartItemCount = 0
  if request.user.is_authenticated:
    order, created = Order.objects.get_or_create(customer=request.user,complete=False)
    cartItemCount = order.orderitem_set.count()
  return cartItemCount

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
  bestSelling = Book.objects.last()
  cartItemCount = getCartItemCount(request)
  quoteResponse = generate_quote()
  context= {
    'books':books, 
    'discountedBooks': discountedBooks,
    'booksByGenre':booksByGenre,
    'coverBooks': coverBooks,
    'bestSelling': bestSelling,
    'user': None,
    'cartItemCount': cartItemCount,
    'quoteOfTheDay': quoteResponse['message'],
    'quotee': quoteResponse['quotee']
  }
  
  return render(request,'base/home.html',context)

def book(request, pk):
  book=Book.objects.get(id=pk)
  context={'book':book, 'cartItemCount': getCartItemCount(request)}
  return render(request,'base/book.html',context)

def loginPage(request):
  user = None
  if request.method=='POST':
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
      user=User.objects.get(email=email)
    except:
      messages.error(request, "User does not exits.")
    
    if user is not None:
      user=authenticate(request,username=user.username, password=password)
      login(request, user)
      request.user = user
      return redirect('home')
    else:
      messages.error(request, "Username or Password  does not match.")

  context={'user': user}
  return render(request, 'base/login.html',context)

def logoutUser(request):
  logout(request)
  return redirect ('/')


def books(request):
  books=Book.objects.all()
  context={'books':books, 'cartItemCount': getCartItemCount(request)}
  return render(request,'base/all_books.html',context)

def offer(request):
  books=Book.objects.filter(discount=False)
  context={'books':books, 'cartItemCount': getCartItemCount(request)}
  return render(request,'base/home.html',context)


def vision(request):
  return render(request,'base/vision.html')

def contact(request):
  return render(request,'base/contact.html')


@login_required(login_url='/login/')
def cart(request):
  if request.user.is_authenticated:
    order, created =Order.objects.get_or_create(customer=request.user,complete=False)
    items=order.orderitem_set.all()
  else:
    items=[]

  context={'items':items, 'order': order, 'cartItemCount': getCartItemCount(request)}
  return render(request,'base/cart.html', context)

@login_required(login_url='/login/')
def order(request, pk):
  order = Order.objects.get(id=pk)
  items = order.orderitem_set.all()
  context = {
    'order': order,
    'items': items,
    'cartItemCount': getCartItemCount(request)
  }
  return render(request, 'base/order.html', context)
  
@login_required(login_url='/login/')
def checkout(request):
  address = request.POST.get("address")
  state = request.POST.get("state")
  city = request.POST.get("city")
  zipcode = request.POST.get("zipcode")
  orderId = request.POST.get("orderId")
  order = Order.objects.get(id=int(orderId))
  shippingAddress = ShippingAddress(address=address, state=state, city=city, zipcode=zipcode, customer=request.user, order=order)
  shippingAddress.save()
  order.complete = True
  order.transaction_id = str(uuid.uuid4())
  order.save()
  return render(request,'base/checkout.html', { 'order': order, 'cartItemCount': getCartItemCount(request) })

@csrf_exempt
def editCart(request):
  editCartBody=json.loads(request.body)
  order, created =Order.objects.get_or_create(customer=request.user,complete=False)
  book=Book.objects.get(id=editCartBody['bookId'])
  orderItem, created = OrderItem.objects.get_or_create(book=book, order=order)
  newQuantity = orderItem.quantity + (editCartBody['quantity'] or 0)
  removeItem = ('removeItem' in editCartBody and editCartBody['removeItem']) or False
  if newQuantity <= 0 or removeItem:
    orderItem.delete()
  else:
    orderItem.quantity = newQuantity
    orderItem.save()
  
  return HttpResponse(json.dumps({ 'success': True, 'cartItemCount': getCartItemCount(request) }), content_type='application/json')

@csrf_exempt
def setCartQuantity(request):
  setCartBody=json.loads(request.body)
  order, created =Order.objects.get_or_create(customer=request.user,complete=False)
  book=Book.objects.get(id=setCartBody['bookId'])
  orderItem, created = OrderItem.objects.get_or_create(book=book, order=order)
  orderItem.quantity = setCartBody['newQuantity']
  orderItem.save()
  return HttpResponse(json.dumps({ 'success': True, 'cartItemCount': getCartItemCount(request) }), content_type='application/json')

@login_required(login_url='/login/')
def order_history(request):
  orders = Order.objects.filter(customer=request.user, complete=True).order_by("-id")
  return render(request,'base/order_history.html', { 'orders': orders, 'cartItemCount': getCartItemCount(request) })

   

