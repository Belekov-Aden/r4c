from django.urls import path

from . import views

urlpatterns = [
    path('', views.RobotsView.as_view(), name='robot_view'),
    path('create-robot/', views.create_robot, name='create_robot'),
    path('generate_excel_report/', views.generate_excel_report, name='generate_excel_report'),
]