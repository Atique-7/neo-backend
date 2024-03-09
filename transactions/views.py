from rest_framework import viewsets, status
from rest_framework.response import Response
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from django.db.models import Q
from users.models import Customer

# Create your views here.
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.query_params.get('start_date'))
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        customer_id = self.request.query_params.get('customer')

        if start_date and end_date:
            queryset = queryset.filter(
                Q(date__gte=start_date), Q(date__lte=end_date)
            )

        # Filter by customer ID directly, if provided 
        if customer_id:
            queryset = queryset.filter(session__customer_id=customer_id)

        print(queryset)

        return queryset
    
    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', True)  # Set partial=True for PATCH
        transaction = self.get_object()
        serializer = self.get_serializer(transaction, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Access updated data from validated serializer data
        updated_data = serializer.validated_data

        # Update transaction fields with existing amounts + new data
        transaction.amount_paid_cash = transaction.amount_paid_cash + updated_data.get('amount_paid_cash', 0)
        transaction.amount_paid_online = transaction.amount_paid_online + updated_data.get('amount_paid_online', 0)


        # Calculate and update derived fields
        total_paid = transaction.amount_paid_cash + transaction.amount_paid_online
        #update debt
        customer = transaction.session.customer
        print(customer)
        customer.debt -= (updated_data.get('amount_paid_cash', 0) + updated_data.get('amount_paid_online', 0))

        customer.save()

        transaction.unpaid_amount = transaction.total_cost - total_paid
        transaction.payment_status = Transaction.FULLY_PAID if total_paid >= transaction.total_cost else Transaction.UNPAID

        # Update payment method logic (optional)
        if transaction.payment_method == Transaction.SPLIT:
            pass  # No change if already split
        else:
            if transaction.payment_method == Transaction.CASH and updated_data.get('amount_paid_online', 0) > 0:
                transaction.payment_method = Transaction.SPLIT
            elif transaction.payment_method == Transaction.ONLINE and updated_data.get('amount_paid_cash', 0) > 0:
                transaction.payment_method = Transaction.SPLIT

        transaction.save()
        return Response(serializer.data)
    
# def update(self, request, pk=None, **kwargs):
#     partial = kwargs.pop('partial', True)
#     transaction = Transaction.objects.get(pk=pk)
    
#     # Get the existing cash and online amounts from the transaction
#     existing_cash_amount = transaction.amount_paid_cash
#     existing_online_amount = transaction.amount_paid_online
    
#     # Get the new cash and online amounts from the request
#     new_cash_amount = request.data.get('amount_paid_cash', 0)
#     new_online_amount = request.data.get('amount_paid_online', 0)
    
#     # Calculate the updated cash and online amounts
#     updated_cash_amount = existing_cash_amount + new_cash_amount
#     updated_online_amount = existing_online_amount + new_online_amount
    
#     # Update the transaction object with the new amounts
#     transaction.amount_paid_cash = updated_cash_amount
#     transaction.amount_paid_online = updated_online_amount
    
#     # Update the unpaid amount based on the total cost and the paid amounts
#     total_cost = transaction.total_cost
#     unpaid_amount = total_cost - (updated_cash_amount + updated_online_amount)
#     transaction.unpaid_amount = unpaid_amount
    
#     # Determine the payment status based on the unpaid amount
#     if unpaid_amount <= 0:
#         transaction.payment_status = Transaction.FULLY_PAID
#     else:
#         transaction.payment_status = Transaction.UNPAID

#     if transaction.payment_method == Transaction.SPLIT:
#         pass
#     else:
#         if transaction.payment_method == Transaction.CASH:    
#             if new_online_amount > 0:
#                 transaction.payment_method = Transaction.SPLIT
#         elif transaction.payment_method == Transaction.ONLINE:
#             if new_cash_amount > 0:
#                 transaction.payment_method = Transaction.SPLIT    
    
#     # Save the updated transaction object
#     transaction.save()
    
#     # Optionally, return a response indicating the update was successful
#     return Response({'message': 'Transaction updated successfully'}, status=status.HTTP_200_OK)
