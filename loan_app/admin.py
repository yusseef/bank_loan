from django.contrib import admin
from .models import CustomUser, LoanProvider, LoanCustomer, BankPersonnel, Loan, LoanApplication, BankSettings

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')
    list_filter = ('role',)
    search_fields = ('username', 'email')

@admin.register(LoanProvider)
class LoanProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_funds')
    search_fields = ('user__username', 'total_funds')

@admin.register(LoanCustomer)
class LoanCustomerAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(BankPersonnel)
class BankPersonnelAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('customer', 'provider', 'amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('customer__user__username', 'provider__user__username')

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'amount_requested', 'status', 'application_date')
    list_filter = ('status',)
    search_fields = ('applicant__username',)

@admin.register(BankSettings)
class BankSettingsAdmin(admin.ModelAdmin):
    list_display = ('min_amount', 'max_amount', 'interest_rate', 'term_months')
    search_fields = ('min_amount', 'max_amount', 'interest_rate')
