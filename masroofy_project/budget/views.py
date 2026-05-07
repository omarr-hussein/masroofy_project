from django.shortcuts import render, redirect
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from .models import BudgetCycle, Expense


def dashboard_view(request):
    """
    User Story #3 + #4 dashboard:
    - Dynamic safe daily limit calculation
    - Visual spending insights by category
    """
    active_cycle = (
        BudgetCycle.objects.filter(is_active=True).order_by("-start_date", "-id").first()
    )

    context = {
        "active_cycle": active_cycle,
        "remaining_budget": Decimal("0.00"),
        "remaining_days": 0,
        "safe_daily_limit": Decimal("0.00"),
        "category_data": [],
        "total_spent": Decimal("0.00"),
    }

    if not active_cycle:
        return render(request, "dashboard.html", context)

    today = timezone.localdate()

    if today > active_cycle.end_date:
        remaining_days = 0
    elif today < active_cycle.start_date:
        remaining_days = (active_cycle.end_date - active_cycle.start_date).days + 1
    else:
        remaining_days = (active_cycle.end_date - today).days + 1

    cycle_expenses = Expense.objects.filter(budget_cycle=active_cycle)
    total_spent = cycle_expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    remaining_budget = active_cycle.total_allowance - total_spent

    if remaining_days > 0:
        safe_daily_limit = remaining_budget / Decimal(remaining_days)
    else:
        safe_daily_limit = Decimal("0.00")

    grouped_expenses = (
        cycle_expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
    )

    category_data = []
    if total_spent > 0:
        for row in grouped_expenses:
            percentage = (row["total"] / total_spent) * Decimal("100")
            category_data.append(
                {
                    "category": row["category"],
                    "total": float(row["total"]),
                    "percentage": float(round(percentage, 2)),
                }
            )

    context.update(
        {
            "remaining_budget": round(remaining_budget, 2),
            "remaining_days": remaining_days,
            "safe_daily_limit": round(safe_daily_limit, 2),
            "category_data": category_data,
            "total_spent": round(total_spent, 2),
        }
    )
    return render(request, "dashboard.html", context)


def transactionsHistory(request):
    transactions = []
    message = ''
    if Expense.objects.count() != 0:
        transactions = Expense.objects.all().order_by('-timestamp')
    else:
        message = 'No transactions found!'

    context = {
        'transactions': transactions,
        'message': message,
    }

    return render(request, 'transactions.html', context)


def create_cycle(request):
    """
    Handles User Story 1: Set Initial Budget Cycle.
    Takes user input and creates a new Budget Cycle in the database.
    """
    if request.method == 'POST':
        total_allowance = Decimal(request.POST.get('total_allowance'))
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        BudgetCycle.objects.update(is_active=False)
        BudgetCycle.objects.create(
            total_allowance=total_allowance,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
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

        active_cycle = (
            BudgetCycle.objects.filter(is_active=True).order_by("-start_date", "-id").first()
        )

        if active_cycle:
            Expense.objects.create(
                budget_cycle=active_cycle,
                amount=amount,
                category=category,
                timestamp=timezone.now(),
            )

        return redirect('dashboard')

    active_cycle = (
        BudgetCycle.objects.filter(is_active=True).order_by("-start_date", "-id").first()
    )
    return render(request, 'budget/log_expense.html', {'no_active_cycle': not active_cycle})