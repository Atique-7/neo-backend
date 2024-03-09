from rest_framework import serializers
from .models import Beverage, Sale

class BeverageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Beverage
    fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Sale
    fields = '__all__'
