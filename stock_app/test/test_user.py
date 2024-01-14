import pytest
from django.core.cache import cache
from rest_framework import status
from rest_framework.test import APIClient
from stock_app.models import User

client = APIClient()


@pytest.mark.django_db
def test_user_create_view():
    data = {
        'username': 'testuser',
        'balance': 100
    }
    url = 'http://localhost:8000/api/users/'
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    username = response.data['username']
    cache_key = f'user_{username}'
    cached_user_data = cache.get(cache_key)
    assert cached_user_data is not None
    assert cached_user_data['username'] == 'testuser'


@pytest.mark.django_db
def test_user_detail_view():
    test_user = User.objects.create(username='testuser', balance=100.0)
    url = f'http://localhost:8000/api/users/{test_user.username}/'
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

    username = response.data['username']
    cache_key = f'user_{username}'
    cached_user_data = cache.get(cache_key)
    assert cached_user_data is not None
    assert cached_user_data['username'] == 'testuser'
