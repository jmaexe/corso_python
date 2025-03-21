from django.utils import timezone
from django.db import models

# Create your models here.

class Person(models.Model) :
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    email = models.EmailField(max_length=100,default="")
    phoneNumber = models.CharField(max_length=10,default="")
    birth_date = models.DateTimeField()
    def __str__(self):
        return self.name + ", " + str(self.age) + ", " + self.email + ", " + self.phoneNumber + ", " +str(self.birth_date) 
