from rest_framework import serializers
from .models import StockData, Transaction, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'balance',)


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('user', 'ticker', 'transaction_type', 'transaction_volume')
