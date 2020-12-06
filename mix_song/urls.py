from django.urls import path
from .import views

app_name = 'mix_song'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("ajax_get_lyrics/", views.IndexView.ajax_get_lyrics, name='ajax_get_lyrics'),
    path('login/', views.LoginView.as_view(), name='login'),
    path("check_password/", views.LoginView.check_password, name='check_password'),
]