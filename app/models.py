from django.db import models
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from django.db.models import Count, Avg, F
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number



@receiver(pre_save, sender=PurchaseOrder)
def update_metrics_on_acknowledgment(sender, instance, **kwargs):
    if instance.acknowledgment_date is not None:
        instance.vendor.average_response_time = calculate_average_response_time(instance.vendor)
        instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_metrics_on_completion(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        instance.vendor.on_time_delivery_rate = calculate_on_time_delivery_rate(instance.vendor)
        instance.vendor.quality_rating_avg = calculate_quality_rating_avg(instance.vendor)
        instance.vendor.fulfillment_rate = calculate_fulfillment_rate(instance.vendor)
        instance.vendor.save()

def calculate_on_time_delivery_rate(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_delivered = completed_orders.filter(delivery_date__lte=timezone.now()).count()
    return on_time_delivered / completed_orders.count() if completed_orders.count() > 0 else 0

def calculate_quality_rating_avg(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed', quality_rating__isnull=False)
    total_ratings = completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg']
    return total_ratings if total_ratings is not None else 0

def calculate_average_response_time(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    total_response_time = sum((order.acknowledgment_date - order.issue_date).total_seconds() for order in completed_orders)
    return total_response_time / completed_orders.count() if completed_orders.count() > 0 else 0

def calculate_fulfillment_rate(vendor):
    total_orders = PurchaseOrder.objects.filter(vendor=vendor)
    successful_fulfillments = total_orders.filter(status='completed').count()
    return successful_fulfillments / total_orders.count() if total_orders.count() > 0 else 0       


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
    
    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


@receiver(post_save, sender=Vendor)
def create_historical_performance(sender, instance, created, **kwargs):
    if created:
        # Automatically create HistoricalPerformance instance
        HistoricalPerformance.objects.create(
            vendor=instance,
            date=timezone.now(),
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfillment_rate=instance.fulfillment_rate
        )

    else:
        # If the Vendor is updated, update the existing HistoricalPerformance instance
        historical_performance = HistoricalPerformance.objects.filter(vendor=instance).latest('date')
        historical_performance.date = timezone.now()
        historical_performance.on_time_delivery_rate = instance.on_time_delivery_rate
        historical_performance.quality_rating_avg = instance.quality_rating_avg
        historical_performance.average_response_time = instance.average_response_time
        historical_performance.fulfillment_rate = instance.fulfillment_rate
        historical_performance.save()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , default=None , null=True)
    firstname = models.CharField(max_length=10 ,null=True, blank=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    # Add other fields as needed

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    print(instance,'-=--=-=--=-=-=-=')
    
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        user_profile.bio = "Default bio"
        user_profile.location = "Default location"
        user_profile.birth_date = "1990-01-01"
        user_profile.save()
        
        