from django.urls import path
from . import views

urlpatterns = [
    # Static Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dogs/<int:dog_id>/add_photo/', views.add_photo, name='add_photo'),
    # Dog Routes
    path('dogs/', views.dogs_index, name='index'),
    path('dogs/<int:dog_id>/', views.dogs_detail, name='detail'),
    path('dogs/<int:dog_id>/edit/', views.edit_dog, name='edit_dog'),
    path('dogs/<int:dog_id>/delete', views.delete_dog, name='delete_dog'),
    path('dogs/new', views.add_dog, name='add_dog'),
    # Feeding Routes
    path('dogs/<int:dog_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    # Toy Routes: associate a toy with a dog (M:M)
    path('dogs/<int:dog_id>/assoc_toy/<int:toy_id>', views.assoc_toys, name='assoc_toys'),
    # Auth Routes
    path('accounts/signup', views.signup, name='signup'),
]