from django.urls import path


from django.urls import * 

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/search", views.search, name="search"),
    path("wiki/<str:title>", views.getEntry, name="title"),
    path("newpage", views.creatNewEntry, name="creatNewEntry"),
    path("wiki/edit/<str:title>", views.edit, name="editPage"),
    path("random", views.random_page, name="randomPage")
]


