from django.shortcuts import render

# Create your views here.
class Dog:
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

dogs = [
  Dog('Zoe', 'Shih Tzu', "the sweetest pup you'll ever meet", 13),
  Dog('Pippin', 'Shih Tzu', 'diluted tortoise shell', 0),
  Dog('Sophie', 'black tripod', '3 legged cat', 4),
  Dog('Lola', 'Shih Tzu', '3 legged cat', 12),
  Dog('Riley', 'Ryans dog', '3 legged cat', 4)
]

# add import
from django.http import HttpResponse

# define the home view
def home(request):
    return HttpResponse('<h1>Hello!</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    return render(request, 'dogs/index.html', { 'dogs': dogs})