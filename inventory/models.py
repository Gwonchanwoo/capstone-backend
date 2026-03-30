from django.db import models

from django.db import models
from django.utils import timezone

# ==========================================
# 1. 기준 정보 (Master Data)
# ==========================================

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="품목 코드")
    name = models.CharField(max_length=100, verbose_name="품목명")
    category = models.CharField(max_length=50, verbose_name="분류")
    selling_price = models.IntegerField(verbose_name="판매 단가")

    def __str__(self):
        return f"[{self.code}] {self.name}"

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="공급업체명")
    lead_time_days = models.IntegerField(verbose_name="입고 소요 기간(일)")

    def __str__(self):
        return self.name

class SupplierPrice(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="공급업체")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    wholesale_price = models.IntegerField(verbose_name="도매 단가")
    min_order_qty = models.IntegerField(verbose_name="최소 발주 수량")

    def __str__(self):
        return f"{self.supplier.name} - {self.product.name}"

# ==========================================
# 2. 운영 데이터 (Operation Data)
# ==========================================

class InventoryBatch(models.Model):
    STATUS_CHOICES = [
        ('NORMAL', '정상'),
        ('EMPTY', '소진'),
        ('DISCARDED', '폐기'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    received_date = models.DateField(verbose_name="입고일자")
    expiration_date = models.DateField(verbose_name="유통기한 만료일자")
    current_qty = models.IntegerField(verbose_name="현재 수량")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NORMAL', verbose_name="상태")

    def __str__(self):
        return f"{self.product.name} (EXP: {self.expiration_date}) - 남은수량: {self.current_qty}"

class SalesHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    sale_datetime = models.DateTimeField(default=timezone.now, verbose_name="판매 일시")
    quantity = models.IntegerField(verbose_name="판매 수량")

    def __str__(self):
        return f"{self.sale_datetime.strftime('%Y-%m-%d %H:%M')} - {self.product.name} ({self.quantity}개)"

class WasteHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    batch = models.ForeignKey(InventoryBatch, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="폐기된 배치")
    waste_datetime = models.DateTimeField(default=timezone.now, verbose_name="폐기 일시")
    quantity = models.IntegerField(verbose_name="폐기 수량")
    reason = models.CharField(max_length=255, verbose_name="폐기 사유")

    def __str__(self):
        return f"[{self.waste_datetime.strftime('%Y-%m-%d')}] {self.product.name} 폐기 ({self.quantity}개)"

# ==========================================
# 3. 예측 및 분석 데이터 (Analytics Data)
# ==========================================

class ExternalFactor(models.Model):
    date = models.DateField(primary_key=True, verbose_name="날짜")
    temperature = models.FloatField(null=True, blank=True, verbose_name="평균 기온")
    precipitation = models.FloatField(null=True, blank=True, verbose_name="강수량")
    is_holiday = models.BooleanField(default=False, verbose_name="공휴일 여부")
    has_promotion = models.BooleanField(default=False, verbose_name="프로모션 여부")
    local_event = models.BooleanField(default=False, verbose_name="지역 행사 여부")

    def __str__(self):
        return str(self.date)

class ForecastResult(models.Model):
    PERIOD_CHOICES = [
        (1, '1일'),
        (2, '2일'),
        (7, '7일'),
        (30, '30일'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="예측 실행 일시")
    target_date = models.DateField(verbose_name="예측 대상 일자")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    predicted_qty = models.FloatField(verbose_name="예상 판매량")
    forecast_period = models.IntegerField(choices=PERIOD_CHOICES, verbose_name="예측 기간")

    def __str__(self):
        return f"{self.target_date} 예측: {self.product.name} ({self.predicted_qty}개)"

class OrderRecommendation(models.Model):
    PRIORITY_CHOICES = [
        ('HIGH', '필수'),
        ('MEDIUM', '권장'),
        ('LOW', '여유'),
    ]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="권고 생성 일시")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="품목")
    recommended_qty = models.IntegerField(verbose_name="권장 발주량")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, verbose_name="우선순위")
    estimated_cost = models.IntegerField(verbose_name="예상 발주 금액")
    reason = models.TextField(verbose_name="권고 사유")

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.product.name} - {self.recommended_qty}개 발주 권고"
