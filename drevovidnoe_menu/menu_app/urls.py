from django.urls import path
from . import views

app_name = 'menu_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('about/team/', views.team, name='team'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
]
