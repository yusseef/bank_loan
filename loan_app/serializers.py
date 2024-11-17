from rest_framework import serializers
from .models import Loan, LoanApplication, BankSettings, CustomUser

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'

class BankSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankSettings
        fields = '__all__'

# Optional: Serializer for the CustomUser model if needed
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'email']
