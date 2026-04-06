from rest_framework import generics
from rest_framework.decorators import api_view  # 👈 새로 추가!
from rest_framework.response import Response    # 👈 새로 추가!
from .models import Product, InventoryBatch, SalesHistory, ForecastResult, Weather # 👈 Weather 추가!
from .serializers import ProductSerializer, InventorySerializer, SalesHistorySerializer, ForecastResultSerializer, WeatherSerializer


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



@api_view(['GET'])
def get_weather(request):
    # 1. 프론트엔드가 주소창에 적은 지역 이름표 확인 (안 적었으면 기본값 '서울')
    target_region = request.GET.get('region', '서울')
    
    # 2. DB에서 그 지역 날씨만 필터링! (시간 순서대로 정렬해서 예쁘게)
    weathers = Weather.objects.filter(region=target_region).order_by('base_date', 'base_time')
    
    # 3. 파이썬 데이터를 프론트엔드용 JSON으로 번역 (데이터가 여러 개니까 many=True)
    serializer = WeatherSerializer(weathers, many=True)
    
    # 4. 프론트엔드로 쏴주기!
    return Response(serializer.data)