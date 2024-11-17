from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('provider', 'Loan Provider'),
        ('customer', 'Loan Customer'),
        ('personnel', 'Bank Personnel'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def is_provider(self):
        return self.role == 'provider'

    def is_customer(self):
        return self.role == 'customer'

    def is_personnel(self):
        return self.role == 'personnel'


class LoanProvider(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    total_funds = models.DecimalField(max_digits=10, decimal_places=2)

class LoanCustomer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class BankPersonnel(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class Loan(models.Model):
    customer = models.ForeignKey(LoanCustomer, on_delete=models.CASCADE)
    provider = models.ForeignKey(LoanProvider, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term_months = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LoanApplication(models.Model):
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, null=True, blank=True)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])
    application_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(null=True, blank=True)


class BankSettings(models.Model):
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
