from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from prova.forms import PersonForm
from prova.models import Person

def index(request):
    return HttpResponse("Hello, world. You're at the index.<a href='people'>people</a></br> ")

def people(request):
    people = Person.objects.all()
    context = {"people": people}
    template = loader.get_template('prova/index.html')
    return HttpResponse(template.render(context,request))

def person(request,id) :
    try:
        person = Person.objects.get(id=id)
    except Person.DoesNotExist: 
        return HttpResponse("Person not found <a href='/'>go back</a")
    return HttpResponse(person)

def form(request,id) :
    person = Person.objects.get(id=id)
    form = PersonForm(instance=person)
    context = {"form": form}
    template = loader.get_template('prova/index.html')
    return HttpResponse(template.render(context,request))

def edit_person(request) :
    a = PersonForm(request.POST)
    print(a.data)
    return HttpResponse("edit person" )

