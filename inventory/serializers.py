from rest_framework import serializers
from .models import Product, InventoryBatch, SalesHistory, ForecastResult  # 🌟 ForecastResult로 수정!

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryBatch
        fields = '__all__'

class SalesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesHistory
        fields = '__all__'

# 🌟 번역기 이름도 ForecastResultSerializer로 맞춤!
class ForecastResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastResult
        fields = '__all__'