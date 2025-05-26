from django.urls import path
from userauth.views import register_view, login_view, account_page, logout_view

urlpatterns = [
    path("signup/", register_view, name="signup"),  
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),   
    path("account/", account_page, name="accountPage"), 
]