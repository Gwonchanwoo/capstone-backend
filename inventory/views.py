from rest_framework import generics
from rest_framework.decorators import api_view  # 👈 기존에 있던 것
from rest_framework.response import Response    # 👈 기존에 있던 것
from django.db.models import Sum                # 👈 (추가) 덧셈 계산을 위한 수학 요리사!
from .models import Product, InventoryBatch, SalesHistory, ForecastResult, Weather
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


# ==========================================
# 🚀 여기서부터 새로 추가된 매출 통계 API!
# ==========================================
@api_view(['GET'])
def get_sales_summary(request):
    target_month = request.GET.get('month', '202512')

    sales_in_month = SalesHistory.objects.filter(sale_date__startswith=target_month)

    category_stats = sales_in_month.values('category').annotate(
        total_qty=Sum('quantity'),
        total_sales=Sum('total_price')
    )

    response_data = {
        "message": f"{target_month} 매출 통계 조회 성공!",
        "data": list(category_stats)
    }

    # 5. 프론트엔드로 깔끔하게 쏴주기!
    return Response(response_data)