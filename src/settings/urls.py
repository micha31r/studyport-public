from django.urls import path
from . import views

app_name = "settings"

urlpatterns = [
    path('app', views.app_view, name="app"),
    path('account', views.account_view, name="account"),
    path('password', views.password_view, name="password"),
    path('theme', views.theme_view, name="theme"),
    path('app/show-mock', views.show_mock_view, name="show-mock"),
    path('app/hide-mock', views.hide_mock_view, name="hide-mock"),
]