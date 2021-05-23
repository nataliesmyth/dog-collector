from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for dog index
    path('dogs', views.dogs_index, name='index'),
]