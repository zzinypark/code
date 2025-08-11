from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet  # posts 앱의 ViewSet 임포트

router = DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")  # basename 지정 베스트 프랙티스

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("rest_framework.urls")),  # 세션 1에서 추가된 부분 유지
    path("api/", include(router.urls)),  # router URL 통합, 모듈화 베스트 프랙티스
]
