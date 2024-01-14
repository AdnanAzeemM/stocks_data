from django.urls import path
from .views import UserCreateView, UserDetailView, StockDataListView, StockDataDetailView, TransactionListView, UserTransactionListView, UserTransactionDateRangeListView

urlpatterns = [
    path('users/', UserCreateView.as_view(), name='user-create'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('stocks/', StockDataListView.as_view(), name='stock-list'),
    path('stocks/<str:ticker>/', StockDataDetailView.as_view(), name='stock-detail'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:user_id>/', UserTransactionListView.as_view(), name='user-transaction-list'),
    path('transactions/<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/', UserTransactionDateRangeListView.as_view(), name='user-transaction-date-range-list'),
]