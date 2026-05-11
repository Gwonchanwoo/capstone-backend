from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Product, InventoryBatch, SalesHistory, ForecastResult, Weather
from .serializers import ProductSerializer, InventorySerializer, SalesHistorySerializer, ForecastResultSerializer, WeatherSerializer
import pandas as pd
from .ai_core.cafe_demand_inventory_model import run_demo # AI 모델 함수 불러오기


# --- 기존 클래스 기반 뷰 (상품, 재고, 판매, 예측 결과 목록) ---
class ProductListCreateAPI(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class InventoryListAPI(generics.ListAPIView):
    queryset = InventoryBatch.objects.all()
    serializer_class = InventorySerializer

class SalesHistoryListCreateAPI(generics.ListCreateAPIView):
    queryset = SalesHistory.objects.all()
    serializer_class = SalesHistorySerializer

class ForecastResultListAPI(generics.ListAPIView):
    queryset = ForecastResult.objects.all()
    serializer_class = ForecastResultSerializer

# --- 기존 날씨 조회 API ---
@api_view(['GET'])
def get_weather(request):
    target_region = request.GET.get('region', '서울')
    weathers = Weather.objects.filter(region=target_region).order_by('base_date', 'base_time')
    serializer = WeatherSerializer(weathers, many=True)
    return Response(serializer.data)

# --- 기존 매출 통계 API ---
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
    return Response(response_data)


# ===========================================================
# 🚀 신규 추가: AI 모델 연동 명세서 규격에 맞춘 예측 API (Mock)
# ===========================================================
@api_view(['POST'])
def predict_future_sales(request):
    """
    프론트엔드에서 받은 요청을 AI 모델에 전달하고,
    그 결과를 명세서 규격에 맞춰 반환하는 진짜 AI 연동 API입니다.
    """
    payload = request.data
    target_date = payload.get('date', '2026-04-07')
    
    try:
        # 1. 🤖 AI 모델 가동 (run_demo 실행)
        # AI 담당자가 준 코드의 기본 설정(GBR 모델, CSV 자동 탐색 등)을 사용합니다.
        print("AI 모델 연산을 시작합니다... 잠시만 기다려 주세요.")
        metrics_df, recommendations_df, feature_df = run_demo(
            model_type="gbr",
            auto_search_csv=True,
            allow_short_history=True, # 데이터가 적어도 실행되도록 설정
            verbose=False
        )

        # 2. 🛠 데이터 클리닝 (결측치 처리)
        # AI 결과에 빈 값(NaN)이 있으면 JSON 변환 시 에러가 나므로 0으로 채워줍니다.
        recommendations_df = recommendations_df.fillna(0)
        feature_df = feature_df.fillna(0) if feature_df is not None else None

        # 3. 📦 AI 결과(표)를 명세서 규격(JSON)으로 변환
        real_results = []
        for _, row in recommendations_df.iterrows():
            real_results.append({
                "date": target_date,
                "item_id": str(row.get('item_id', 'unknown')),
                "q50_daily": round(float(row.get('q50_daily', row.get('q50', 0))), 2),
                "q95_daily": round(float(row.get('q95_daily', row.get('q95', 0))), 2),
                "protection_days": int(row.get('protection_days', 4)),
                "target_stock": round(float(row.get('target_stock', 0)), 2),
                "recommended_order_qty": int(row.get('recommended_order_qty', 0))
            })

        # 4. 📊 예측 근거(Feature Importance) 변환
        real_feature_importance = []
        if feature_df is not None and not feature_df.empty:
            # 상위 5개 주요 요인만 추출
            for _, row in feature_df.head(5).iterrows():
                cols = feature_df.columns
                real_feature_importance.append({
                    "feature": str(row[cols[0]]), 
                    "importance_percentage": round(float(row[cols[1]]), 2)
                })

        print("✅ AI 예측 및 데이터 변환이 성공적으로 완료되었습니다.")

        # 5. 최종 응답 발송
        return Response({
            "status": "success",
            "results": real_results,
            "feature_importance": real_feature_importance
        })

    except Exception as e:
        # 에러 발생 시 로그 출력 및 프론트엔드에 알림
        print(f"🚨 AI 연동 오류 발생: {e}")
        return Response({
            "status": "error",
            "message": "AI 모델 실행 중 문제가 발생했습니다.",
            "error_detail": str(e)
        }, status=500)