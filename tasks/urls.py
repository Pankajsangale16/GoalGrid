from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('', views.dashboard, name='dashboard'),
    path('client/create/', views.client_create, name='client_create'),
    path('client/delete/<int:pk>/', views.client_delete, name='client_delete'),
    path('client/<int:client_id>/task/create/', views.task_create, name='task_create'),
    path('task/toggle/<int:pk>/', views.task_toggle, name='task_toggle'),
    path('task/delete/<int:pk>/', views.task_delete, name='task_delete'),
]
