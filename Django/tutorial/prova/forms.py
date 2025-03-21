from django.utils import timezone
from django.forms import ModelForm, SelectDateWidget

from prova.models import Person 

class PersonForm(ModelForm) :
    class Meta:
        model = Person
        fields="__all__"
        widgets={
            "birth_date" : SelectDateWidget(years=range(timezone.now().year - 150,timezone.now().year))
        }

   