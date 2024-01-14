import pytest
from rest_framework import status
from rest_framework.test import APIClient
from stock_app.models import StockData, Transaction, User

client = APIClient()


@pytest.fixture
def sample_stock_data():
    return {
        'ticker': 'test',
        'open_price': 150.00,
        'close_price': 160.00,
        'high': 165.00,
        'low': 145.00,
        'volume': 100000,
        'timestamp': '2022-01-01T12:00:00Z',
    }


@pytest.mark.django_db
def test_create_buy_transaction(sample_stock_data):
    sample_user = User.objects.create(username='testuser', balance=1000.0)
    StockData.objects.create(**sample_stock_data)

    url = 'http://localhost:8000/api/transactions/'
    data = {
        'user': sample_user.user_id,
        'ticker': 'test',
        'transaction_type': 'buy',
        'transaction_volume': 5,
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Check if the user's balance is updated correctly
    sample_user.refresh_from_db()
    assert sample_user.balance == 1000.0 - 160.0 * 5


@pytest.mark.django_db
def test_create_sell_transaction(sample_stock_data):
    sample_user = User.objects.create(username='testuser2', balance=1000.0)
    StockData.objects.create(**sample_stock_data)

    url = 'http://localhost:8000/api/transactions/'
    data = {
        'user': sample_user.user_id,
        'ticker': 'test',
        'transaction_type': 'sell',
        'transaction_volume': 5,
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Check if the user's balance is updated correctly
    sample_user.refresh_from_db()
    assert sample_user.balance == 1000.0 + 160.0 * 5


@pytest.mark.django_db
def test_check_invalid_transaction_type(sample_stock_data):
    sample_user = User.objects.create(username='testuser2', balance=1000.0)
    StockData.objects.create(**sample_stock_data)

    url = 'http://localhost:8000/api/transactions/'
    data = {
        'user': sample_user.user_id,
        'ticker': 'test',
        'transaction_type': 'invalid',
        'transaction_volume': 5,
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_insufficient_balance_for_transaction(sample_stock_data):
    sample_user = User.objects.create(username='testuser1', balance=100)
    StockData.objects.create(**sample_stock_data)
    url = 'http://localhost:8000/api/transactions/'
    data = {
        'user': sample_user.user_id,
        'ticker': sample_stock_data['ticker'],
        'transaction_type': 'sell',
        'transaction_volume': 10,
    }

    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_get_transaction_sing_user_id(sample_stock_data):
    test_user = User.objects.create(username='testuser_', balance=1200)
    StockData.objects.create(**sample_stock_data)
    Transaction.objects.create(
        user=test_user, ticker='test', transaction_type='buy', transaction_volume=1, transaction_price=100.0
    )
    url = f'http://localhost:8000/api/transactions/{test_user.user_id}'

    response = client.get(url)
