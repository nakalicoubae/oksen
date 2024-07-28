from django.urls import path
from . import views
from .views import login_view

app_name = 'weightroom'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('checklist/', views.checklist, name='checklist'),
    path('usage_time/', views.usage_time, name='usage_time'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
]