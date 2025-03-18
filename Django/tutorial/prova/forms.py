from django.forms import ModelForm

from prova.models import Person 

class PersonForm(ModelForm) :
    class Meta:
        model = Person
        fields = ["name","age","email","phoneNumber"]

   