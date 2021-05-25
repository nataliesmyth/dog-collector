from main_app.forms import FeedingForm
from django.shortcuts import render
from .models import Dog

# Create your views here.

# add import
from django.http import HttpResponse

# define the home view
def home(request):
    return HttpResponse('<h1>Hello!</h1>')

def about(request):
    return render(request, 'about.html')

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', { 'dogs': dogs })

# the dogs_detail function is using the get method to obtain the dog object by its id
# Django will pass any captured URL parameters as a named argument to the view function
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    # instantiate FeedingForm to be rendered in templates
    feeding_form = FeedingForm()
    return render(request, 'dogs/detail.html', { 
        'dog': dog, 'feeding_form': feeding_form 
        })

def add_feeding(request, dog_id):
    # pass is a way to define an 'empty' python function
    pass