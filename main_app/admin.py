from django.contrib import admin
# import models here
from .models import Dog, Feeding

# Register your models here.
admin.site.register(Dog)
admin.site.register(Feeding)