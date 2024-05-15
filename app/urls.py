from django.urls import path
from app.views import *
from .import views

urlpatterns = [

        path('v',VenderApiview.as_view()),
        path('v/<int:id>',VenderApiview.as_view()),
        path('vd/<int:vid>',VenderApiview.as_view()),

        path('p',PurchaseorderApi.as_view()),
        path('p/<int:id>',PurchaseorderApi.as_view()),
        path('vp/<int:vid>',PurchaseorderApi.as_view()),

        path('h',HistoricalPerApi.as_view()),
        path('h/<int:id>',HistoricalPerApi.as_view()),

]       
