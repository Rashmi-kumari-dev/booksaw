from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('book/<str:pk>/',views.book, name="book"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('books/', views.books, name="books"),
    path('vision/',views.vision,name="vision"),
    path('contact/',views.contact,name="contact"),
    path('cart/',views.cart,name="cart"),
    path('editCart/', views.edit_cart, name="editCart"),
    path('order_history/', views.order_history, name="order_history"),
    path('checkout/', views.checkout, name="checkout"),
    path('setCartQuantity/', views.set_cart_quantity, name="setCartQuantity"),
    path('order/<str:pk>/', views.order, name="order"),
]