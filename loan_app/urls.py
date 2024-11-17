from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanProviderViewSet, LoanCustomerViewSet, BankPersonnelViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'loan-providers', LoanProviderViewSet, basename='loan-provider')
router.register(r'loan-customers', LoanCustomerViewSet, basename='loan-customer')
router.register(r'bank-personnel', BankPersonnelViewSet, basename='bank-personnel')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
