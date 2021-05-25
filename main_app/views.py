from main_app.forms import FeedingForm
from django.shortcuts import render, redirect
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
  # create the ModelForm using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the dog_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)

# note: always use redirect, not render, if data has been changed in the database.