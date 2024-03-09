from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer, BeverageSerializer
from .models import Beverage
from transactions.models import Transaction
from users.models import Customer

class BeverageListCreate(generics.ListCreateAPIView):
    queryset = Beverage.objects.all()
    serializer_class = BeverageSerializer

class BeverageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Beverage.objects.all()
    serializer_class = BeverageSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Assuming the request data contains customer_id, beverage_id, and quantity
        customer_id = request.data.get('customer_id')
        beverage_id = request.data.get('beverage_id')
        quantity = request.data.get('quantity')

        try:
            customer = Customer.objects.get(id=customer_id)
            beverage = Beverage.objects.get(id=beverage_id)

            # Check if enough inventory is available
            if beverage.inventory < quantity:
                return Response({'message': 'Not enough inventory available'}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total cost of the sale
            total_cost = beverage.price * quantity

            # Assuming payment method and status are provided in the request data
            payment_method = request.data.get('payment_method')
            payment_status = request.data.get('payment_status')

            # Calculate amounts paid in cash and online
            amount_paid_cash = request.data.get('amount_paid_cash', 0)
            amount_paid_online = request.data.get('amount_paid_online', 0)

            # Calculate unpaid amount
            unpaid_amount = total_cost - (amount_paid_cash + amount_paid_online)

            # Create Sale instance
            sale = Sale.objects.create(
                customer=customer,
                beverage=beverage,
                quantity=quantity
            )

            # Create Transaction instance
            transaction = Transaction.objects.create(
                session=None,  # Assuming session is not relevant for sale transactions
                food=True,  # Set food bool to True
                food_sale=sale,  # Add the sale instance
                total_cost=total_cost,
                payment_method=payment_method,
                unpaid_amount=unpaid_amount,
                amount_paid_cash=amount_paid_cash,
                amount_paid_online=amount_paid_online,
                payment_status=payment_status
            )

            # Update remaining inventory of the beverage
            beverage.inventory -= quantity
            beverage.save()
            transaction.save()

            return Response({'message': 'Sale created successfully'}, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({'message': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        except Beverage.DoesNotExist:
            return Response({'message': 'Beverage not found'}, status=status.HTTP_404_NOT_FOUND)
