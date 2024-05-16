from django.urls import path
from app.views import *
from .import views

urlpatterns = [
        # this three urls for vender data get,update,delete,insert 
        path('vender',VenderApiview.as_view()),
        path('vender/<int:id>',VenderApiview.as_view()),
        path('venderid/<int:vid>',VenderApiview.as_view()),
        
        # this three urls for purchaseorder data get,update,delete,insert 
        path('purchas',PurchaseorderApi.as_view()),
        path('purchas/<int:id>',PurchaseorderApi.as_view()),
        path('purchasvid/<int:vid>',PurchaseorderApi.as_view()),
       
       # this two urls for vender-performance data get 
        path('performance',HistoricalPerApi.as_view()),
        path('performancevender/<int:id>',HistoricalPerApi.as_view()),

]       
