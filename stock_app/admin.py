from django.contrib import admin
from .models import User, StockData, Transaction


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'balance', 'email', 'first_name', 'last_name', 'is_staff')


class StockDataAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'open_price', 'close_price', 'high', 'low', 'volume', 'timestamp')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'transaction_type', 'transaction_volume', 'transaction_price', 'timestamp')


admin.site.register(User, UserAdmin)
admin.site.register(StockData, StockDataAdmin)
admin.site.register(Transaction, TransactionAdmin)
