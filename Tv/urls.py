from django.urls import path
from Tv import views

urlpatterns = [
    path('', views.SeriesView, name="SeriesView"),
    path('add/', views.SeriesAddView, name="SeriesAddView"),
    
    path('<slug:slug>/', views.SeriesDetailView, name="SeriesDetailView"),
    path('<slug:slug>/season/<slug:season_slug>/', views.SeasonDetailView, name="SeasonDetailView"),
    # path('<slug:slug>/season/<slug:season_slug>/episode/<slug:episode_slug>/', views.EpisodeDetailView, name="EpisodeDetailView"),
]