from django.urls import path, include
from rest_framework.routers import DefaultRouter
from session.views import SessionViewSet

router = DefaultRouter()
router.register(r'session', SessionViewSet, basename='sessions')

urlpatterns = [
    path('', include(router.urls)),
]
