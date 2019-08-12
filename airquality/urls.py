from django.urls import path, include
from . import views

app_name = 'airquality'  # used to differentiate namespaces when multiple apps exist

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('logout/', views.logout_view, name='logout'),
 #   path('<int:pk>/', views.DetailView.as_view(), name='detail'),
 #   path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
 #   path('<int:question_id>/vote/', views.vote, name='vote'),
]
