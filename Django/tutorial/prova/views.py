from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template import loader

from prova.forms import  PersonForm
from prova.models import Person

def index(request):
    return HttpResponse("Hello, world. You're at the index.<a href='people'>people</a></br> ")

def people(request):
    people = Person.objects.all()
    if request.method == "POST" : 
        id = request.POST.get("id")
        person =get_object_or_404(Person,id=id) 
        person.delete()
    context = {"people": people}
    return render(request,"prova/people.html",context)

def person(request,id) :
    person = get_object_or_404(Person,id=id)
    return HttpResponse(person)


def edit_person(request,id) :
    person = Person.objects.get(id=id)
    if request.method == "POST" : 
        form = PersonForm(request.POST,instance=person)
        if form.is_valid() : 
            form.save()
            return HttpResponseRedirect("/prova/people")

    form = PersonForm(instance=person)
    context = {"form": form,"id": id,"labelForm" : "Edit Person","url" : "prova:edit_person"}
    return render(request,"prova/PersonForm.html",context)

def add_person(request) : 
    if request.method == "POST" : 
        form = PersonForm(request.POST)
        if form.is_valid() : 
            form.save()
            return HttpResponseRedirect("/prova/people") 
    else : 
        form = PersonForm()
    context = {"form": form,"labelForm" : "Add Person", "url": "prova:add_person"}
    template = loader.get_template('prova/PersonForm.html')
    return HttpResponse(template.render(context,request))