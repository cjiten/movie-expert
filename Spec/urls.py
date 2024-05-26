from django.urls import path
from Spec import views

urlpatterns = [
    path('', views.HomeView, name="HomeView"),

    path('genre/<slug:slug>/', views.GenerView, name="GenerView"),
    path('category/<slug:slug>/', views.CategoryView, name="CategoryView"),

    path('link/<slug:slug>/send/', views.LinkSendView, name="LinkSendView"),
    path('link/<slug:slug>/r/', views.LinkReceiveView, name="LinkReceiveView"),
]
