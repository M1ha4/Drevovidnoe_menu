from django.urls import path
from . import views

app_name = 'menu_app'  # 👈 должно совпадать с namespace в include

urlpatterns = [
    path('', views.menu_view, name='menu'),
]
