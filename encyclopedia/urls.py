from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="singleentry"),
    path("results", views.results, name="results"),
    path("create", views.create, name="new_entry"),
    path("edit", views.edit, name="edit_entry")
]
