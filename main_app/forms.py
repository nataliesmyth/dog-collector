from django import forms
from .models import Dog, Feeding

# Feeding Form
class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']

# Dog Form
class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ('name', 'breed', 'description', 'age') # Tuple is preferred to keep data consistent