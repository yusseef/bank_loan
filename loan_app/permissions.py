from rest_framework.permissions import BasePermission

class IsLoanProvider(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'provider'

class IsLoanCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'customer'

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'personnel'
