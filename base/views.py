from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Book, Genre, Order, OrderItem, ShippingAddress
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .service.book_service import BookService
from .service.quote_service import QuoteService
from .service.cart_service import CartService
from .service.order_service import OrderService
from .forms import SignupForm

def home(request):
  books = BookService.find_all_featured()
  discountedBooks = BookService.find_all_discounted()
  booksByGenre = BookService.find_all_genre_groups()
  coverBooks = BookService.find_all_covers()
  bestSelling = BookService.find_best_selling()
  cartItemCount = CartService.get_items_count(request.user)
  quoteResponse = QuoteService.generate()
  context= {
    'books':books,
    'discountedBooks': discountedBooks,
    'booksByGenre':booksByGenre,
    'coverBooks': coverBooks,
    'bestSelling': bestSelling,
    'cartItemCount': cartItemCount,
    'quoteOfTheDay': quoteResponse['message'],
    'quotee': quoteResponse['quotee']
  }
  
  return render(request,'base/home.html',context)

def books(request):
  books = BookService.find_all()
  context = { 'books': books, 'cartItemCount': CartService.get_items_count(request.user) }
  return render(request,'base/all_books.html', context)

def book(request, pk):
  book = BookService.find_by_id(pk)
  context={'book':book, 'cartItemCount': CartService.get_items_count(request.user)}
  return render(request,'base/book.html',context)

@login_required(login_url='/login/')
def cart(request):
  cart_response = CartService.get_cart_for_user(request.user)

  context = {
    'items': cart_response['items'], 
    'order': cart_response['order'], 
    'cartItemCount': CartService.get_items_count(request.user)
  }
  return render(request,'base/cart.html', context)

@csrf_exempt
def edit_cart(request):
  edit_cart_request = json.loads(request.body)
  CartService.edit_cart(request.user, edit_cart_request)
  
  return HttpResponse(json.dumps({ 'success': True, 'cartItemCount': CartService.get_items_count(request.user) }), content_type='application/json')

@csrf_exempt
def set_cart_quantity(request):
  set_cart_request = json.loads(request.body)
  CartService.set_cart_quantity(request.user, set_cart_request)
  return HttpResponse(json.dumps({ 'success': True, 'cartItemCount': CartService.get_items_count(request.user) }), content_type='application/json')

@login_required(login_url='/login/')
def checkout(request):
  address = request.POST.get("address")
  state = request.POST.get("state")
  city = request.POST.get("city")
  zipcode = request.POST.get("zipcode")
  orderId = request.POST.get("orderId")
  order = Order.objects.get(id=int(orderId))

  shipping_address = ShippingAddress(address=address, state=state, city=city, zipcode=zipcode, customer=request.user, order=order)
  CartService.checkout(order, shipping_address)

  return render(request,'base/checkout.html', { 'order': order, 'cartItemCount': CartService.get_items_count(request.user) })

@login_required(login_url='/login/')
def order(request, pk):
  order = OrderService.find_by_id(pk)
  items = OrderService.find_all_items(order)
  context = {
    'order': order,
    'items': items,
    'cartItemCount': CartService.get_items_count(request.user)
  }
  return render(request, 'base/order.html', context)

@login_required(login_url='/login/')
def order_history(request):
  orders = OrderService.get_order_history_for_user(request.user)
  return render(request,'base/order_history.html', { 'orders': orders, 'cartItemCount': CartService.get_items_count(request.user) })

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
  else:
      form = SignupForm()
  return render(request, 'base/signup.html', {'form': form})

def login_page(request):
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
      if user is None:
        messages.error(request, "Username or Password  does not match.")
        return render(request, 'base/login.html')
      login(request, user)
      request.user = user
      return redirect('home')
    else:
      messages.error(request, "Username or Password  does not match.")

  context={'user': user}
  return render(request, 'base/login.html',context)

def logout_user(request):
  logout(request)
  return redirect ('/')

def vision(request):
  return render(request,'base/vision.html')

def contact(request):
  return render(request,'base/contact.html')
