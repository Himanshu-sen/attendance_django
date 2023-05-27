from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Contact(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    phone= models.CharField(max_length=15)
    desc= models.TextField()
    date= models.DateField()

    def __str__(self):
        return self.name
class Attendance(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    department = models.CharField(max_length=100, null="NA")
    year = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default='Absent')
    
    def __str__(self):
        return self.name
    
class faces(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='static/images/', null=True)

    def __str__(self):
        return self.name
    

