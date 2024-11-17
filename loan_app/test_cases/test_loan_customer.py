from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from loan_app.models import Loan, LoanCustomer, LoanProvider

User = get_user_model()

class LoanCustomerTestCase(APITestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user(username="customer", password="customer123", role="customer")
        self.customer = LoanCustomer.objects.create(user=self.customer_user)

        self.provider_user = User.objects.create_user(username="provider", password="provider123", role="provider")
        self.provider = LoanProvider.objects.create(user=self.provider_user, total_funds=20000)

        response = self.client.post('/api/token/', {
            'username': 'customer',
            'password': 'customer123'
        })
        self.token = response.data['access']

        self.url = "/api/loan-customers/"

    def test_view_loans(self):
        Loan.objects.create(
            customer=self.customer,
            provider=self.provider,
            amount=5000,
            term_months=12,
            interest_rate=5.0,
            status="approved"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_make_payment(self):
        loan = Loan.objects.create(
            customer=self.customer,
            provider=self.provider,
            amount=5000,
            term_months=12,
            interest_rate=5.0,
            status="approved"
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(f"{self.url}{loan.id}/make-payment/", {"amount": 1000})
        self.assertEqual(response.status_code, 200)
        loan.refresh_from_db()
        self.assertEqual(loan.amount, 4000)
