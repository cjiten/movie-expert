from django.urls import path
from Movie import views

urlpatterns = [
    path('', views.MovieView, name="MovieView"),
    path('add/', views.MovieAddView, name="MovieAddView"),
    
    path('<slug:slug>/', views.MovieDetailView, name="MovieDetailView"),
]