from django.urls import path
from api.views import login

urlpatterns = [
    path('login/', login.LoginView.as_view()),
    path('register/', login.RegisterView.as_view()),
]