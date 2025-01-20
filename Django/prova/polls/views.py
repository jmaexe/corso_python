from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
def index(request) : 
    users =  User.objects.all()
    template = loader.get_template('index.html')
    return HttpResponse(template.render({'users': users},request))