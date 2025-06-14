from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('face-login/', views.face_login, name='face_login'),
    path('login/', views.login_view, name='login'),
]
