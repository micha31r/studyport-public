from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path('', views.list_view, name="list"),
    path('create', views.create_view, name="create"),
    path('edit/<int:pk>', views.edit_view, name="edit"),
    path('delete/<str:pks>', views.delete_view, name="delete"),
]