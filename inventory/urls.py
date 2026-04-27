from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductListCreateAPI.as_view()),
    path('inventory/', views.InventoryListAPI.as_view()),
    path('sales/', views.SalesHistoryListCreateAPI.as_view()),
    # 🌟 연결할 뷰 이름 변경!
    path('forecasts/', views.ForecastResultListAPI.as_view()), 
    path('weather/', views.get_weather, name='get_weather'),
    
    # 🚀 새로 추가: 프론트엔드가 호출할 월별 매출 통계 대문!
    path('sales/summary/', views.get_sales_summary, name='sales_summary'),
    
]