from django.urls import path
from . import views

app_name = "usermgmt"

urlpatterns = [
    path('login', views.custom_oauth2_login, name="login"),
    path('login/password', views.password_login_view, name="password-login"),
    path('logout', views.logout_view, name="logout"),
    path('account-migration', views.account_migration_view, name="account-migration"),
]