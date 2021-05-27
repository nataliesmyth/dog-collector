from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# A tuple of 2-tuples
# The first item in each 2-tuple represents the value that will be stored in the database
# The second item represents teh human friendly "display" value
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# TOY MODEL
class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

# DOG MODEL
class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Custom Join Table
# class Dog_Toys():
#   date = models.DateField() # We can our own properties
#   dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
#   toy = models.ForeignKey(Toy, on_delete=models.CASCADE)

# FEEDING MODEL
class Feeding(models.Model):
    date = models.DateField('feeding date')
    meal = models.CharField(
        'Dog Meal',
        max_length=1,
        # add the 'choices' field option
        choices=MEALS,
        # set the default value for meal to be 'B'
        default=MEALS[0][0]
        )
        # Create a dog_id foreign key(FK)
        # First argument provides the parent model
        # The second argument on_delete=models.CASCADE is required; it ensures that if a Dog record is deleted, all of the child Feedings will be deleted automatically as well, avoiding orphan records.
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

# change the default order so most recent dates are displayed on top
class Meta:
    ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for dog_id: {self.dog_id} @{self.url}"