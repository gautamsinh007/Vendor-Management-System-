from  .models import *
from rest_framework import serializers
from django.contrib.auth.models  import User


class VenderSerializers(serializers.ModelSerializer):
     class Meta:
        model = Vendor
        fields =  "__all__"


class PurchaseOrderSerializers(serializers.ModelSerializer):
     class Meta:
        model = PurchaseOrder
        fields =  "__all__"


class HistoricalPerSerializers(serializers.ModelSerializer):
     class Meta:
        model = HistoricalPerformance
        fields =  "__all__"
