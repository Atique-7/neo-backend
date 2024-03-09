from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sales', views.SaleViewSet, basename='sale')

urlpatterns = [
    path('beverages/', views.BeverageListCreate.as_view(), name='beverage-list-create'),
    path('beverages/<int:pk>/', views.BeverageRetrieveUpdateDestroy.as_view(), name='beverage-retrieve-update-destroy'),
    path('', include(router.urls)),
]
