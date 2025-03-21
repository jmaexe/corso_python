from django.urls import path

from . import views
app_name = "prova"
urlpatterns = [
    path("", views.index, name="index"),
    path("people",views.people, name="people"),
    path("people/<int:id>",views.person,name="person"),
    path("people/<int:id>/edit-person",views.edit_person,name="edit_person"),
    path("people/add-person",views.add_person,name="add_person"),
]