from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import date
from decimal import Decimal
from .models import Cycle, Transaction

def calculate_days_left(cycle):
    """Calculates days remaining in the active budget cycle."""
    today = date.today()
    if today > cycle.end_date:
        return 0
    return (cycle.end_date - today).days

def create_cycle(request):
    """
    Handles User Story 1: Set Initial Budget Cycle.
    Takes user input and creates a new Budget Cycle in the database.
    """
    if request.method == 'POST':
        total_amount = Decimal(request.POST.get('total_amount'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        Cycle.objects.create(
            total_amount=total_amount,
            start_date=start_date,
            end_date=end_date,
            current_balance=total_amount
        )
        return redirect('dashboard')
        
    return render(request, 'budget/create_cycle.html')

def log_expense(request):
    """
    Handles User Story 2: Rapid Expense Logging.
    Logs a new transaction and deducts the amount from the cycle's balance.
    """
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        category = request.POST.get('category')
        
        active_cycle = Cycle.objects.last()
        
        if active_cycle:
            Transaction.objects.create(
                cycle=active_cycle,
                amount=amount,
                category=category,
                date=timezone.now().date()
            )
            active_cycle.current_balance -= amount
            active_cycle.save()
            
        return redirect('dashboard')
        
    return render(request, 'budget/log_expense.html')