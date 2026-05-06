from django.db import models
from django.utils import timezone


class BudgetCycle(models.Model):
    """Stores the user's budgeting cycle and initial allowance."""

    total_allowance = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-start_date", "-id"]

    def __str__(self):
        return f"Budget cycle {self.start_date} to {self.end_date}"


class Expense(models.Model):
    """Represents a logged expense inside a budget cycle."""

    class Category(models.TextChoices):
        FOOD = "Food", "Food"
        TRANSPORT = "Transport", "Transport"
        UTILITIES = "Utilities", "Utilities"
        ENTERTAINMENT = "Entertainment", "Entertainment"
        OTHER = "Other", "Other"

    budget_cycle = models.ForeignKey(
        BudgetCycle,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=Category.choices)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp", "-id"]

    def __str__(self):
        return f"{self.category}: {self.amount}"