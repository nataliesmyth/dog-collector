from django.shortcuts import render, HttpResponse, redirect
from .forms import FeedingForm, DogForm
from .models import Dog, Toy, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
def dogs_index(request):
    dogs = Dog.objects.all()
    context = {
        'dogs': dogs
    }
    return render(request, 'dogs/index.html', context)

# DOGS SHOW/DETAIL ROUTE
# the function below uses the get method to obtain the dog object by its id
# Django will pass any captured URL parameters as a named argument to the view function
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

# DOGS NEW ROUTE
    # combined view function like this one
    # When creating something in the database we need a 
    # We call it combined because it handles both POST (or 
    # DELETE or PUT) and GET requests
def new_dog(request):
# If a post request is made to this view function
    if request.method == 'POST':
    # We save the form data to a new variable
        form = DogForm(request.POST)
    # We make sure the data passes validations
    if form.is_valid():
        # If it does, associate cat with logged in user and 
        # save it in the database
        dog = form.save(commit=False)
        dog.user = request.user
        dog.save()
        # Redirect the user to the new cat's detail page
        return redirect('detail', dog.id)
    else:
    # If it's a get request, load the form from forms.py
        form = DogForm()
        # Save the form to a new variable
        context = { 'form': form }
        # Render the cat form template with the form
        return render(request, 'dogs/dog_form.html', context)

# DOG DELETE ROUTE
def delete_dog(request, dog_id):
    # dog = Dog.objects.get(id=dog_id)
    # dog.delete()
    Dog.objects.get(id=dog_id).delete()
    return redirect('index')

# DOG ADD FEEDING ROUTE
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

# Dog Add Toys Route
def assoc_toys(request, dog_id, toy_id):
    # You can also pass a toy's id instead of the whole object
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect('detail', dog_id=dog_id)


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