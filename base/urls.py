from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('book/<str:pk>/',views.book, name="book"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('books/', views.books, name="books"),
    path('offer/',views.offer,name="offer"),
    path('vision/',views.vision,name="vision"),
    path('contact/',views.contact,name="contact"),
    path('report_problem/',views.report_problem,name="report_problem"),
    path('cart/',views.cart,name="cart"),
    path('editCart/', views.editCart, name="editCart"),
    path('order_history/', views.order_history, name="order_history"),
    path('checkout/', views.checkout, name="checkout"),
    path('setCartQuantity/', views.setCartQuantity, name="setCartQuantity"),
    path('order/<str:pk>/', views.order, name="order"),

]