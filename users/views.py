from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
  queryset = Customer.objects.all()
  serializer_class = CustomerSerializer

  def get_queryset(self):
    queryset = super().get_queryset()
    username = self.request.query_params.get('username', None)
    if username:
      queryset = queryset.filter(username__icontains=username)
    return queryset
  
  def post(self, request):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)