from django.contrib import admin
from django.urls import path, include  # 🌟 include 라는 마법의 단어가 추가되었습니다!

urlpatterns = [
    path('admin/', admin.site.urls),                     # 기존에 있던 관리자 페이지 주소
    path('api/', include('inventory.urls')),             # 🌟 새로 추가된 API 입구!
]