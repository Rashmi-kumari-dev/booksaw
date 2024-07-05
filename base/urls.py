from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('book/<str:pk>/',views.book, name="book"),
    path('login/', views.login, name="login"),
    path('books/', views.books, name="books"),
]