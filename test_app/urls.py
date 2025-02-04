
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/lift-data/', views.lift_data_api, name='lift-data-api'),
]
