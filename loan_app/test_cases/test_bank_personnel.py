from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from loan_app.models import Loan, LoanCustomer, LoanProvider

User = get_user_model()
class BankPersonnelTestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.customer_user = User.objects.create_user(username="customer", password="customer123", role="customer")
        self.customer = LoanCustomer.objects.create(user=self.customer_user)

        self.provider_user = User.objects.create_user(username="provider", password="provider123", role="provider")
        self.provider = LoanProvider.objects.create(user=self.provider_user, total_funds=20000)

        self.personnel_user = User.objects.create_user(username="personnel", password="personnel123", role="personnel")

        # Obtain JWT token for the bank personnel
        response = self.client.post('/api/token/', {
            'username': 'personnel',
            'password': 'personnel123'
        })
        self.token = response.data['access']

        self.url = "/api/bank-personnel/"

    def test_check_total_loan_limit(self):
        # Create a loan for the customer with a valid provider
        Loan.objects.create(
            customer=self.customer,
            provider=self.provider,
            amount=15000,
            term_months=12,
            interest_rate=3.5,
            status="approved"
        )

        # Include the token in the Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        response = self.client.get(f"{self.url}total-loan-limit-check/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Funds are within limit", response.data["status"])
