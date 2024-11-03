from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.generate_main_report, name='generate_main_report'),
    path('last-month', views.generate_last_month_report, name='generate_last_month_report'),
]
