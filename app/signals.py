# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .utils import update_on_time_delivery_rate, update_quality_rating_avg, update_average_response_time, update_fulfilment_rate 
# # from .models import PurchaseOrder



# @receiver(post_save, sender=PurchaseOrder)
# def purchase_order_post_save(sender, instance, created, **kwargs):
#     if created or instance.status_changed:
#         update_on_time_delivery_rate(instance.vendor)
#         update_quality_rating_avg(instance.vendor)
#         update_average_response_time(instance.vendor)
#         update_fulfilment_rate(instance.vendor)
