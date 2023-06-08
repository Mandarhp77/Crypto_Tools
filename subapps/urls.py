from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('price/', views.price, name='price'),
    path('price', views.price, name='price'),
    path('home/', views.home, name='home'),
    path('listing/', views.listing, name='listing'),
    path('listing', views.listing, name='listing'),
    path('recent/', views.recent, name='recent'),
    path('recent', views.recent, name='recent'),
    path('price2/', views.price2, name='price2'),
    path('price2', views.price2, name='price2'),
]