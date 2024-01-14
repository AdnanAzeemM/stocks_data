import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.core.cache import cache
from stock_app.models import StockData

client = APIClient()


@pytest.fixture
def sample_stock_data():
    return {
        "ticker": "test",
        "open_price": 150,
        "close_price": 155.0,
        "high": 160.0,
        "low": 145.0,
        "volume": 100000,
        "timestamp": "2024-01-01T12:00:00Z"
    }


@pytest.mark.django_db
def test_stock_data_list_view(sample_stock_data):
    StockData.objects.create(**sample_stock_data)
    url = 'http://localhost:8000/api/stocks/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_stock_data_create_view(sample_stock_data):
    url = 'http://localhost:8000/api/stocks/'
    response = client.post(url, data=sample_stock_data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert StockData.objects.filter(ticker=sample_stock_data['ticker']).exists()
    cached_data = cache.get('stock_test')
    assert cached_data is not None
    assert response.data == cached_data


@pytest.mark.django_db
def test_stock_data_detail_view_with_cache(sample_stock_data):
    stock_instance = StockData.objects.create(**sample_stock_data)
    url = f'http://localhost:8000/api/stocks/{stock_instance.ticker}/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    cached_data = cache.get('stock_test')
    assert cached_data is not None
    assert response.data['ticker'] == stock_instance.ticker
    assert response.data['volume'] == stock_instance.volume


@pytest.mark.django_db
def test_stock_data_list_view_with_cache():
    url = f'http://localhost:8000/api/stocks/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0
    cached_data = cache.get('stock_data')


@pytest.mark.django_db
def test_stock_data_list_view_without_cache():
    cache.clear()
    url = f'http://localhost:8000/api/stocks/'
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    cached_data = cache.get('stock_data')
    assert cached_data is not None


@pytest.mark.django_db
def test_stock_data_detail_view_not_found():
    url = f'http://localhost:8000/api/stocks/abc/'
    response = client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"error": "Item not found"}
