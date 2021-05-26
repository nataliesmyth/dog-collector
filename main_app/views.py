from django.shortcuts import render, HttpResponse, redirect
from .forms import FeedingForm
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

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', { 'dogs': dogs })

# the dogs_detail function is using the get method to obtain the dog object by its id
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
    # print(f"Dog ID = {dog_id}, Toy ID = {toy_id}")
    dog = Dog.objects.get(id=dog_id)
    toy = Toy.objects.get(id=toy_id)
    dog.toys.add(toy)
    return redirect('detail', dog_id)


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