# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .tasks import process_transaction
# from .models import Transaction
#
#
# @receiver(post_save, sender=Transaction)
# def on_transaction_created(sender, instance, created, **kwargs):
#     if created:
#         process_transaction.delay(instance.id)
