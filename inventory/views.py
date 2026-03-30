from rest_framework import generics
from .models import Product, InventoryBatch, SalesHistory, ForecastResult
from .serializers import ProductSerializer, InventorySerializer, SalesHistorySerializer, ForecastResultSerializer

class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryListAPI(generics.ListAPIView):
    queryset = InventoryBatch.objects.all()
    serializer_class = InventorySerializer

class SalesHistoryListCreateAPI(generics.ListCreateAPIView):
    queryset = SalesHistory.objects.all()
    serializer_class = SalesHistorySerializer

# 🌟 뷰 이름도 ForecastResultListAPI로 맞춤!
class ForecastResultListAPI(generics.ListAPIView):
    queryset = ForecastResult.objects.all()
    serializer_class = ForecastResultSerializer