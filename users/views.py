from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.decorators import action

class CustomerViewSet(viewsets.ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer

  def get_queryset(self):
    queryset = super().get_queryset()
    # total_customers = queryset.length()
    username = self.request.query_params.get('username', None)
    debt = self.request.query_params.get('debt', None)

    if username:
      queryset = queryset.filter(username__icontains=username)
    if debt:
      queryset = queryset.filter(debt__gt=0).order_by('-debt')
    return queryset
  
  @action(detail=False, methods=['get'])
  def total_customers(self, request):
        total_customers = self.request.query_params.get('totalCustomers', None)
        total_customers = self.get_queryset().count()
        return Response({'total_customers': total_customers})
  
  def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)