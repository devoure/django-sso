from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name="index"),
        path('/dater/show/', views.showdate, name="showdate")
        ]
