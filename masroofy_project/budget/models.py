from django.db import models
from django.utils import timezone

class Cycle(models.Model):
    """
    Represents a budget cycle in the Masroofy application.
    
    This model acts as the core entity tracking the overall budget allowance, 
    the timeframe (start and end dates), and the current remaining balance 
    for the student.
    """
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Returns a string representation of the Cycle."""
        return f"Budget Cycle: {self.start_date} to {self.end_date}"


class Transaction(models.Model):
    """
    Represents a single financial transaction (expense) within a budget cycle.
    """
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        """Returns a string representation of the Transaction."""
        return f"{self.category} Expense: {self.amount} EGP"