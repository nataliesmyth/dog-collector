from django.shortcuts import render, HttpResponse, redirect
from .models import Dog, Toy, Photo
from .forms import FeedingForm, DogForm
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import uuid
import boto3

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'pupcollector'

# HOME ROUTE
def home(request):
    return render(request, 'home.html')

# ABOUT ROUTE
def about(request):
    return render(request, 'about.html')

# CONTACT ROUTE
def contact(request):
    return render(request, 'basic/contact.html')

# DOGS INDEX ROUTE
@login_required
def dogs_index(request):
    # Query below retrieves the logged in users dogs
    dogs = Dog.objects.filter(user=request.user)
    context = {
        'dogs': dogs
    }
    return render(request, 'dogs/index.html', context)

# DOGS SHOW/DETAIL ROUTE
# the function below uses the get method to obtain the dog object by its id
# Django will pass any captured URL parameters as a named argument to the view function
@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    # Get toys the dog doesn't have
    toys_dog_doesnt_have = Toy.objects.exclude(id__in=dog.toys.all().values_list('id'))
    # instantiate FeedingForm to be rendered in templates
    feeding_form = FeedingForm()
    context = {
        'dog': dog,
        'feeding_form': feeding_form,
        'toys': toys_dog_doesnt_have,
    }
    return render(request, 'dogs/detail.html', context)

# DOG EDIT/UPDATE ROUTE
@login_required
def edit_dog(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    # GET - Edit Dog
    # POST - Update Dog
    if request.method == 'POST':
        form = DogForm(request.POST, instance=dog)
        if form.is_valid():
            dog = form.save()
            return redirect('detail', dog.id)
    else:
        # Create Form
        form = DogForm(instance=dog)
        # Render Form
        return render(request, 'dogs/edit.html', {'form': form})

# DOGS NEW ROUTE WITH CUSTOM FORM
@login_required
def add_dog(request):
  if request.method == 'POST':
    # Can we print out one piece of data from the request?
    # print('Name = ', request.POST['name'])

    # Pull Dog data out of request.POST
    name = request.POST['name']
    breed = request.POST['breed']
    description = request.POST['description']
    age = request.POST['age']

    # Create new instance of Dog object
    new_dog = Dog(name=name, breed=breed, description=description, age=age)
    form = DogForm(request.POST)
    new_dog = form.save(commit=False)
    # Associate User and Dog
    new_dog.user = request.user
    # Save new Dog in DB
    new_dog.save()

    return redirect('detail', new_dog.id)
  else:
    form = DogForm()
    return render(request, 'dogs/new.html', {'form': form})



# Dogs New Route with Class Based Form
# @login_required
# def add_dog(request):
#   if request.method == 'POST':
#     form = DogForm(request.POST)
#     if form.is_valid():
#       new_dog = form.save(commit=false)
#       # Associate User and Dog
#       new_dog.user = request.user
#       # Save new Dog in DB
#       new_dog.save()
#       return redirect('detail', new_dog.id)
#   else:
#     form = DogForm()
#     return render(request, 'dogs/new.html', {'form': form})

# DOG DELETE ROUTE
@login_required
def delete_dog(request, dog_id):
    # dog = Dog.objects.get(id=dog_id)
    # dog.delete()
    Dog.objects.get(id=dog_id).delete()
    return redirect('index')

# DOG ADD FEEDING ROUTE
@login_required
def add_feeding(request, dog_id):
    # create the ModelForm using the data in request.POST
    form = FeedingForm(request.POST)
    # validate the form
    if form.is_valid():
    # don't save the form to the db until it has the dog_id assigned
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
        # note: always use redirect, not render, if data has been changed in the database.
        return redirect('detail', dog_id=dog_id)
    else:
        return redirect('detail', dog_id=dog_id)

# DOG ADD TOY ROUTE
@login_required
def assoc_toys(request, dog_id, toy_id):
    # You can also pass a toy's id instead of the whole object
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect('detail', dog_id=dog_id)

# SIGN UP ROUTE
# User Signup Route
def signup(request):
  error = None
  form = UserCreationForm()
  context = {
    'form': form,
    'error': error,
  }
  if request.method == 'POST':
    # Create an instance of Form
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      return render(request, 'registration/signup.html', {'form': form, 'error': form.errors})
  else:
    return render(request, 'registration/signup.html', context)


def add_photo(request, dog_id):
    # photo-fie will be the 'name' attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # We need a unique 'key' for S3 and an image file extension
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to dog_id or dog (if  you have a dog object)
            photo = Photo(url=url, dog_id=dog_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
    # return redirect('detail', dog_id=dog_id)