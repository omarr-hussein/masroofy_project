from django.shortcuts import render, redirect
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from .models import BudgetCycle, Expense


def dashboard_view(request):
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
        "threshold_level": None,
        "expenditure_percentage": 0,
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
            category_data.append({
                "category": row["category"],
                "total": float(row["total"]),
                "percentage": float(round(percentage, 2)),
            })

    # Budget threshold notification
    expenditure_percentage = 0
    threshold_level = None
    if active_cycle.total_allowance > 0:
        expenditure_percentage = float((total_spent / active_cycle.total_allowance) * 100)
        if expenditure_percentage >= 90:
            threshold_level = "critical"
        elif expenditure_percentage >= 75:
            threshold_level = "warning"

    context.update({
        "remaining_budget": round(remaining_budget, 2),
        "remaining_days": remaining_days,
        "safe_daily_limit": round(safe_daily_limit, 2),
        "category_data": category_data,
        "total_spent": round(total_spent, 2),
        "threshold_level": threshold_level,
        "expenditure_percentage": round(expenditure_percentage, 1),
    })
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


def todaysBudget(request):
    today = timezone.localdate()
    active_cycle = (
        BudgetCycle.objects.filter(is_active=True).order_by("-start_date", "-id").first()
    )

    if not active_cycle:
        return render(request, 'todaysBudget.html', {'no_active_cycle': True, 'today': today})

    cycleExpenses = Expense.objects.filter(budget_cycle=active_cycle)
    totalSpent = cycleExpenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    remainingBudget = active_cycle.total_allowance - totalSpent

    # Remaining days
    if today > active_cycle.end_date:
        remainingDays = 0
    elif today < active_cycle.start_date:
        remainingDays = (active_cycle.end_date - active_cycle.start_date).days + 1
    else:
        remainingDays = (active_cycle.end_date - today).days + 1

    if remainingDays > 0:
        safeDailyLimit = remainingBudget / Decimal(remainingDays)
    else:
        safeDailyLimit = Decimal("0.00")

    yesterday = today - timezone.timedelta(days=1)
    totalCycleDays = (active_cycle.end_date - active_cycle.start_date).days + 1
    base_daily = active_cycle.total_allowance / Decimal(totalCycleDays) if totalCycleDays > 0 else Decimal("0.00")

    yesterdaySpent = cycleExpenses.filter(
        timestamp__date=yesterday
    ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    rolloverAmount = max(base_daily - yesterdaySpent, Decimal("0.00"))

    todaysExpenses = cycleExpenses.filter(timestamp__date=today).order_by('-timestamp')
    spent_today = todaysExpenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    adjusted_daily_limit = safeDailyLimit + rolloverAmount
    remaining_today = adjusted_daily_limit - spent_today
    over_limit = spent_today > adjusted_daily_limit

    if adjusted_daily_limit > 0:
        progress_pct = float((spent_today / adjusted_daily_limit) * 100)
    else:
        progress_pct = 0

    expenditure_percentage = 0
    threshold_level = None
    if active_cycle.total_allowance > 0:
        expenditure_percentage = float((totalSpent / active_cycle.total_allowance) * 100)
        if expenditure_percentage >= 90:
            threshold_level = "critical"
        elif expenditure_percentage >= 75:
            threshold_level = "warning"

    context = {
        'today': today,
        'active_cycle': active_cycle,
        'safe_daily_limit': round(adjusted_daily_limit, 2),
        'spent_today': round(spent_today, 2),
        'remaining_today': round(remaining_today, 2),
        'remaining_budget': round(remainingBudget, 2),
        'todays_expenses': todaysExpenses,
        'over_limit': over_limit,
        'progress_pct': round(progress_pct, 1),
        'rollover_amount': round(rolloverAmount, 2) if rolloverAmount > 0 else None,
        'threshold_level': threshold_level,
        'expenditure_percentage': round(expenditure_percentage, 1),
        'no_active_cycle': False,
    }
    return render(request, 'todaysBudget.html', context)