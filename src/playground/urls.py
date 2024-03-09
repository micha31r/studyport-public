from django.urls import path
from . import views

app_name = "playground"

urlpatterns = [
    path('', views.list_view, name="list"),
    path('activate', views.activate_view, name="activate"),
    path('deactivate', views.deactivate_view, name="deactivate"),
    path('select/<int:pk>', views.select_view, name="select"),
    path('create', views.create_view, name="create"),
    path('create/<str:activate>', views.create_view, name="create"),
    path('edit/<int:pk>', views.edit_view, name="edit"),
    path('delete/<int:pk>', views.delete_view, name="delete"),
]