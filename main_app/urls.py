from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # route for dog index
    path('dogs', views.dogs_index, name='index'),
    # route for dog detail page
    path('dogs/<int:dog_id>/', views.dogs_detail, name='detail'),
    path('dogs/<int:dog_id>/add_feeding/', views.add_feeding, name='add_feeding'),
]