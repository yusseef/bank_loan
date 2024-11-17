from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from loan_app.models import LoanProvider, LoanApplication

User = get_user_model()

class LoanProviderTestCase(APITestCase):
    def setUp(self):
        self.provider_user = User.objects.create_user(username="provider", password="provider123", role="provider")
        self.provider = LoanProvider.objects.create(user=self.provider_user, total_funds=10000)

        response = self.client.post('/api/token/', {
            'username': 'provider',
            'password': 'provider123'
        })
        self.token = response.data['access']

        self.url = "/api/loan-providers/"

    def test_view_loan_applications(self):
        LoanApplication.objects.create(applicant=self.provider_user, amount_requested=5000, status="pending")

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
