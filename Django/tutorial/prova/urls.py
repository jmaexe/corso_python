from django.urls import path

from . import views
app_name = "prova"
urlpatterns = [
    path("", views.index, name="index"),
    path("people",views.people, name="people"),
    path("people/<int:id>",views.person,name="person"),
    path("people/<int:id>/form",views.form,name="form"),
    path("people/edit-person",views.edit_person,name="edit_person"),
]