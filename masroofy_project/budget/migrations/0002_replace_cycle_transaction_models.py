import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("budget", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BudgetCycle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_allowance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["-start_date", "-id"]},
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Food", "Food"),
                            ("Transport", "Transport"),
                            ("Utilities", "Utilities"),
                            ("Entertainment", "Entertainment"),
                            ("Other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "budget_cycle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="expenses",
                        to="budget.budgetcycle",
                    ),
                ),
            ],
            options={"ordering": ["-timestamp", "-id"]},
        ),
        migrations.DeleteModel(name="Transaction"),
        migrations.DeleteModel(name="Cycle"),
    ]
