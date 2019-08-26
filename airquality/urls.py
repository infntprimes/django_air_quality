from django.urls import path, include
from . import views

app_name = 'airquality'  # used to differentiate namespaces when multiple apps exist

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
]