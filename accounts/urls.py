from django.urls import path
from .views import *

urlpatterns = [
    path("",home_view,name="home"),
    path("register/",register_view,name="register"),
    path("login/",login_view,name="login"),
    path("logout/",logout_view,name="logout"),
    path("profile/",profile_view,name="profile"),
    path("confirm/<uuid:token>/",confirm_token_view,name='confirm'),  
    path("change-password/", change_password_view, name="change_password"),
    path("reset-password/", reset_password_view, name="reset_password"),
    path("reset-password/<uuid:token>/", confirm_reset_password_view, name="confirm_reset_password"),
    path("resend-email/", resend_email_view, name="resend_email"),
    path("resend-reset-email/", resend_reset_email_view, name="resend_reset_email"),

]
