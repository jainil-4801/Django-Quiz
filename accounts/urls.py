from django.urls import path
from .api import LoginAPI, RegisterAPI, UserAPI, LogoutAPI

urlpatterns = [
    path("login/", LoginAPI.as_view(),name="login"),
	path("register/", RegisterAPI.as_view(),name="register"),
	path("user/", UserAPI.as_view(),name="user"),
	path("logout/",LogoutAPI,name="logout")
]
