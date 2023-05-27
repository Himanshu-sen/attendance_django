from django import forms
from .models import *
from django.core.validators import RegexValidator

class registration(forms.ModelForm):

    name= forms.CharField(label='name',
                          min_length=5,
                          max_length=50,
                          validators=[RegexValidator(r'^[a-zA-Z0-9]*$',message="please only letters are allowed!")])