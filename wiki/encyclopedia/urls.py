from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("new-page", views.newpage, name="newpage"),
    path("newpage", views.newpage, name="newpage"),
    path("savepage", views.savepage, name="savepage"),
    path("editpage", views.editpage, name="editpage"),
    path("saveeditpage", views.saveeditpage, name="saveeditpage"),
    path("randompage", views.randompage, name="randompage"),
]
