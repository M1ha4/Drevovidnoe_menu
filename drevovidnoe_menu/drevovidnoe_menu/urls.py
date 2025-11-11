from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('about/history/', TemplateView.as_view(template_name='history.html'), name='history'),
    path('about/team/', TemplateView.as_view(template_name='team.html'), name='team'),
    path('services/', TemplateView.as_view(template_name='services.html'), name='services'),
    path('services/dev/', TemplateView.as_view(template_name='dev.html'), name='dev'),
    path('services/analytics/', TemplateView.as_view(template_name='analytics.html'), name='analytics'),
    path('contacts/', TemplateView.as_view(template_name='contacts.html'), name='contacts'),

    path('menu/', include(('menu_app.urls', 'menu_app'), namespace='menu_app')),
]
