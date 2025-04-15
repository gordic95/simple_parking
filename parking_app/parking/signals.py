# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from . models import Parkings
#
#
#
# @receiver(post_save, sender=Parkings)
# def payment_complete(sender, instance, created, **kwargs):
#     if created:
#         instance.calculate_price_on_time()
#
