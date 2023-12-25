from django.db import models
from ..user.models import CustomUser as User
from django.core.validators import MinValueValidator, MaxValueValidator

class Expense(models.Model):
    """
        Expense Model for adding expense to expense table
    """
    SPLIT_TYPE_CHOICES = [
        ('Equal', 'Equal'),
        ('Percent', 'Percent'),
        ('Exact', 'Exact'),
    ]

    payer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    total_amount_spend = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10000000)],
        null=False
    )
    split_type = models.CharField(
        max_length=10,
        choices=SPLIT_TYPE_CHOICES,
        default='Equal'
    )
    date = models.DateTimeField(auto_now_add=True)

class Passbook(models.Model):
    """
        Passbook Model for adding payment entries to the passbook table
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True)