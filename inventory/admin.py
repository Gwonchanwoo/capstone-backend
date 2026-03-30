from django.contrib import admin
from .models import (
    Product, Supplier, SupplierPrice, InventoryBatch, 
    SalesHistory, WasteHistory, ExternalFactor, 
    ForecastResult, OrderRecommendation
)

# 캡스톤 프로젝트 관리자 페이지를 보기 편하게 커스텀합니다.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'selling_price') # 목록에서 보여줄 기준
    search_fields = ('code', 'name') # 검색 기능 추가
    list_filter = ('category',) # 우측 필터 기능 추가

@admin.register(InventoryBatch)
class InventoryBatchAdmin(admin.ModelAdmin):
    list_display = ('product', 'received_date', 'expiration_date', 'current_qty', 'status')
    list_filter = ('status', 'expiration_date')
    search_fields = ('product__name',)

@admin.register(SalesHistory)
class SalesHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale_datetime', 'quantity')
    list_filter = ('sale_datetime',)

@admin.register(WasteHistory)
class WasteHistoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'waste_datetime', 'quantity', 'reason')
    list_filter = ('reason', 'waste_datetime')

@admin.register(ExternalFactor)
class ExternalFactorAdmin(admin.ModelAdmin):
    list_display = ('date', 'temperature', 'precipitation', 'is_holiday', 'has_promotion', 'local_event')
    list_filter = ('is_holiday', 'has_promotion')

@admin.register(ForecastResult)
class ForecastResultAdmin(admin.ModelAdmin):
    list_display = ('target_date', 'product', 'predicted_qty', 'forecast_period', 'created_at')
    list_filter = ('forecast_period', 'target_date')

@admin.register(OrderRecommendation)
class OrderRecommendationAdmin(admin.ModelAdmin):
    list_display = ('product', 'recommended_qty', 'priority', 'estimated_cost', 'created_at')
    list_filter = ('priority',)

# Supplier와 SupplierPrice는 기본 형태로 등록
admin.site.register(Supplier)
admin.site.register(SupplierPrice)