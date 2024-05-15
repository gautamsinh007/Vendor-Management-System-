from django.shortcuts import render 
from rest_framework import routers, serializers, viewsets
from .models import *
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import * 
from  rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
# this is 

class VenderApiview(APIView):

    def get(self, request, id=None, vid=None):
        try:
            if id:
                vendor = Vendor.objects.get(id=id)
                serializer = VenderSerializers(vendor)
                return Response(serializer.data)
            elif vid:
                vendor = Vendor.objects.get(vendor_code=vid)
                serializer = VenderSerializers(vendor)
                return Response(serializer.data)

            else:
                vendors = Vendor.objects.all()
                serializer = VenderSerializers(vendors, many=True)
                return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = VenderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            serializer = VenderSerializers(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            vendor = Vendor.objects.get(id=id)
            vendor.delete()
            return Response("Vendor deleted", status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response("Vendor not found", status=status.HTTP_404_NOT_FOUND)

   

class PurchaseorderApi(APIView):


   
    def get(self, request, id=None,  vid=None):
        try:
            if id:
                purchase = PurchaseOrder.objects.get(id=id)
                serializer = PurchaseOrderSerializers(purchase)
                return Response(serializer.data)
            
            elif vid:
                vendor = PurchaseOrder.objects.filter(vendor=vid)
                serializer = PurchaseOrderSerializers(vendor, many=True)
                return Response(serializer.data)

            else:
                purchase = PurchaseOrder.objects.all()
                serializer = PurchaseOrderSerializers(purchase, many=True)
                return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response("purchaseorder not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = PurchaseOrderSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            purchase = PurchaseOrder.objects.get(id=id)
            serializer = PurchaseOrderSerializers(purchase, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response("purchaseorder not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            purchase = PurchaseOrder.objects.get(id=id)
            purchase.delete()
            return Response("purchaseorder deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("purchaseorder dddnot found", status=status.HTTP_404_NOT_FOUND)


class HistoricalPerApi(APIView):

    def get(self, request, id=None):
        try:
            if id:
                histo = HistoricalPerformance.objects.get(id=id)
                serializer = HistoricalPerSerializers(histo)
                return Response(serializer.data)
            else:
                histo = HistoricalPerformance.objects.all()
                serializer = HistoricalPerSerializers(histo, many=True)
                return Response(serializer.data)
        except HistoricalPerformance.DoesNotExist:
            return Response("HistoricalPerformance not found", status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = HistoricalPerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id):
        try:
            histo = HistoricalPerformance.objects.get(id=id)
            serializer = HistoricalPerSerializers(histo, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except HistoricalPerformance.DoesNotExist:
            return Response("HistoricalPerformance not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            histo = HistoricalPerformance.objects.get(id=id)
            histo.delete()
            return Response("HistoricalPerformance deleted", status=status.HTTP_204_NO_CONTENT)
        except:
            return Response("HistoricalPerformance dddnot found", status=status.HTTP_404_NOT_FOUND)

