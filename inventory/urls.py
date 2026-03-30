from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListCreateAPI.as_view()),
    path('inventory/', views.InventoryListAPI.as_view()),
    path('sales/', views.SalesHistoryListCreateAPI.as_view()),
    # 🌟 연결할 뷰 이름 변경!
    path('forecasts/', views.ForecastResultListAPI.as_view()), 
]