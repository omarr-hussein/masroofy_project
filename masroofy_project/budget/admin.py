from django.contrib import admin
from .models import BudgetCycle, Expense


@admin.register(BudgetCycle)
class BudgetCycleAdmin(admin.ModelAdmin):
    list_display = ("id", "total_allowance", "start_date", "end_date", "is_active")
    list_filter = ("is_active", "start_date", "end_date")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "budget_cycle", "amount", "category", "timestamp")
    list_filter = ("category", "timestamp")
    search_fields = ("category",)
