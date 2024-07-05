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
]