# loan_app/views.py

from decimal import Decimal
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Loan, LoanApplication, LoanProvider, LoanCustomer
from .serializers import LoanSerializer, LoanApplicationSerializer
from .permissions import IsLoanProvider, IsLoanCustomer, IsBankPersonnel
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LoanProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Loan Provider can view the status of their loan fund applications.
    """
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsLoanProvider]

    def get_queryset(self):
        return LoanApplication.objects.filter(applicant=self.request.user)


class LoanCustomerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Loan Customer can view their loan applications and make payments for their loans.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated, IsLoanCustomer]

    def get_queryset(self):
        return Loan.objects.filter(customer__user=self.request.user)

    @action(detail=True, methods=['post'], url_path='make-payment')
    def make_payment(self, request, pk=None):
        """
        Loan Customer can make a payment towards their loan balance.
        """
        loan = self.get_object()
        amount = request.data.get('amount')

        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = Decimal(amount)
        except:
            return Response({"error": "Invalid amount format"}, status=status.HTTP_400_BAD_REQUEST)

        if loan.amount - amount >= 0:
            loan.amount -= amount
            loan.save()
            return Response({"status": "Payment successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Payment exceeds loan balance"}, status=status.HTTP_400_BAD_REQUEST)


class BankPersonnelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Bank Personnel can view applications from loan providers and customers, and ensure the total loan limit is within the fund limit.
    """
    queryset = LoanApplication.objects.all()
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsBankPersonnel]

    def get_queryset(self):
        return LoanApplication.objects.all()

    @action(detail=False, methods=['get'], url_path='total-loan-limit-check')
    def total_loan_limit_check(self, request):
        """
        Bank Personnel can check if total loans exceed available funds.
        """
        total_funds = sum(provider.total_funds for provider in LoanProvider.objects.all())
        total_loans = sum(loan.amount for loan in Loan.objects.all())

        if total_loans > total_funds:
            return Response({"error": "Total loans exceed available funds"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": "Funds are within limit"}, status=status.HTTP_200_OK)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['role'] = user.role  # Assuming the `role` is a field in your User model
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role  # Add role to the response
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
