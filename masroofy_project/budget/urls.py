from django.urls import path
from . import views

urlpatterns = [
    path('create-cycle/', views.create_cycle, name='create_cycle'),
    path('log-expense/', views.log_expense, name='log_expense'),
    path('todaysBudget/' , views.calculateTodayBudget , name='todaysBudget'),
    path('transactions/', views.transactionsHistory, name='transactions'),
]