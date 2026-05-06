from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('create-cycle/', views.create_cycle, name='create_cycle'),
    path('log-expense/', views.log_expense, name='log_expense'),
    path('dashboard/', views.dashboard_view, name='dashboard_page'),
    path('transactions/', views.transactionsHistory, name='transactions'),
]