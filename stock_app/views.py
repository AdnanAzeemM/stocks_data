from rest_framework import generics, status
from .serializers import *
from django.core.cache import cache
from rest_framework.response import Response


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user_instance = serializer.save()
        user_data = UserSerializer(user_instance).data
        cache_key = f'user_{user_instance.username}'
        try:
            cache.set(cache_key, user_data, timeout=3600)
        except Exception as e:
            print(f"Error setting data in cache: {e}")


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'username'

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user_data = cache.get(f'user_{username}')
        if not user_data:
            try:
                queryset = User.objects.get(username=username)
                user_data = UserSerializer(queryset).data
                cache.set(f'user_{username}', user_data, timeout=3600)
            except User.DoesNotExist:
                pass
            except Exception as e:
                print(f"Error fetching data from database: {e}")
        return Response(user_data)


class StockDataListView(generics.ListCreateAPIView):
    queryset = StockData.objects.all()
    serializer_class = StockSerializer

    def list(self, request, *args, **kwargs):
        all_stock_data = [cache.get(key) for key in cache.keys('*stock*')]
        if all_stock_data:
            return Response(all_stock_data)
        else:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set('stock_data', data, timeout=3600)
            return Response(data)

    def perform_create(self, serializer):
        serializer.save()
        data = serializer.data
        cache.set(f'stock_{data["ticker"]}', data, timeout=3600)


class StockDataDetailView(generics.RetrieveAPIView):
    queryset = StockData.objects.all()
    serializer_class = StockSerializer
    lookup_field = 'ticker'

    def retrieve(self, request, *args, **kwargs):
        ticker = self.kwargs.get('ticker')
        stock_item = cache.get(f'stock_{ticker}')
        if stock_item is not None:
            return Response(stock_item)
        try:
            instance = StockData.objects.get(ticker=ticker)
            serializer = StockSerializer(instance)
            data = serializer.data
            cache.set(f'stock_{data["ticker"]}', data, timeout=3600)
            return Response(data)
        except StockData.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)


class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        ticker = serializer.validated_data['ticker']
        transaction_type = serializer.validated_data['transaction_type']
        transaction_volume = serializer.validated_data['transaction_volume']

        try:
            stock_data = StockData.objects.filter(ticker=ticker).latest('timestamp')
        except StockData.DoesNotExist:
            return Response({"error": "Stock data not found"}, status=status.HTTP_404_NOT_FOUND)

        transaction_price = stock_data.close_price * transaction_volume

        if transaction_type == 'sell' and user.balance < transaction_price:
            return Response({"error": "Insufficient balance for sell transaction"}, status=status.HTTP_400_BAD_REQUEST)

        if transaction_type == 'buy':
            user.balance -= transaction_price
        elif transaction_type == 'sell':
            user.balance += transaction_price

        user.save()
        user.refresh_from_db()
        serializer.validated_data['transaction_price'] = transaction_price
        transaction = serializer.save()

        # Update user data in cache after the transaction
        username = user.username
        user_data = cache.get(f'user_{username}')
        if user_data:
            user_data['balance'] = user.balance
            cache.set(f'user_{username}', user_data, timeout=3600)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)


class UserTransactionListView(generics.RetrieveAPIView):
    serializer_class = TransactionListSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        return Transaction.objects.filter(user__user_id=user_id)


class UserTransactionDateRangeListView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        start_timestamp = self.kwargs['start_timestamp']
        end_timestamp = self.kwargs['end_timestamp']
        return Transaction.objects.filter(user__user_id=user_id, timestamp__range=[start_timestamp, end_timestamp])
