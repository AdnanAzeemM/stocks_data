from celery import shared_task
from django.core.cache import cache


@shared_task
def process_transaction(transaction_id):
    from .models import StockData, Transaction
    try:
        transaction_instance = Transaction.objects.get(pk=transaction_id)

        user = transaction_instance.user
        ticker = transaction_instance.ticker
        stock_data = StockData.objects.filter(ticker=ticker).latest('timestamp')
        transaction_price = stock_data.close_price

        if transaction_instance.transaction_type == 'buy' and user.balance >= transaction_price:
            user.balance -= transaction_price
            user.save()

            transaction_instance.transaction_price = transaction_price
            transaction_instance.save()

            # Update user data in cache after processing the transaction
            username = user.username
            user_data = cache.get(f'user_{username}')
            if user_data:
                user_data['balance'] = user.balance
                cache.set(f'user_{username}', user_data, timeout=3600)

        else:
            pass
    except Exception as e:
        print(f"Error processing transaction {transaction_id}: {e}")
