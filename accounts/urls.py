from django.urls import path
from .views import (
    register,
    logIn,
    logOut,
)


urlpatterns = [
    path('login/', logIn, name='login_page'),
    path('logout/', logOut, name='logout_page'),
    path('registration/', register, name='registration_page')
]
