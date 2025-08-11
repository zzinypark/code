from django.urls import path, include
from rest_framework import routers

from blog.views import api_view_set_views

app_name = "view_set_api"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", api_view_set_views.UserViewSet, basename="users")
router.register(r"blogs", api_view_set_views.BlogViewSet, basename="blogs")

urlpatterns = [
    path("", include(router.urls)),
]
