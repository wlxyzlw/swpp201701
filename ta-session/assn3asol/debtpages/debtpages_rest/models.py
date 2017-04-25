from django.db import models

# Create your models here.

class Debt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    borrower = models.ForeignKey('auth.User', related_name='debts_as_borrower', on_delete=models.CASCADE)
    lender = models.ForeignKey('auth.User', related_name='debts_as_lender', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created', )


