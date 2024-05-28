from rest_framework import viewsets, status
from rest_framework.response import Response

from session.models import Session, Pricing
from session.serializers import SessionSerializer

from users.models import Customer
from transactions.models import Transaction


class SessionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save()

            try:
                pricing = Pricing.objects.get(session_type=session.session_type)
                price_per_unit = pricing.price_per_unit
                price_per_frame = pricing.price_per_frame
                duration_minutes = pricing.duration_minutes
            except Pricing.DoesNotExist:
                return Response({'error': 'Pricing for this session type not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            tokens_available = None            
            if session.session_type == "PS5":
                tokens_available = session.customer.ps5_tokens
            elif session.session_type == "PS4":
                tokens_available = session.customer.ps4_tokens

            response_data = {
                'session_id': session.id,
                'price_per_unit': price_per_unit,
                'price_per_frame': price_per_frame,
                'duration_minutes' : duration_minutes,
                'tokens_available' : tokens_available
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def update(self, request, pk):
    #     try:
    #         session = Session.objects.get(pk=pk)
    #         customer = session.customer

    #         actual_duration = request.data.get('actual_duration')
    #         planned_duration = request.data.get('planned_duration')
    #         tokens_saved = request.data.get('tokens_saved')
    #         tokens_spent = request.data.get('tokens_spent')
    #         amount = request.data.get('amount')
    #         online = request.data.get('online')
    #         cash = request.data.get('cash')

    #         session.actual_duration = actual_duration
    #         session.planned_duration = planned_duration
    #         session.save()

    #         total_cost = int(amount)
    #         amount_paid = int(online) + int(cash)
    #         unpaid_amount = max(total_cost - amount_paid, 0)

    #         if (int(cash) > 0) and (int(online) > 0):
    #             payment_method = Transaction.SPLIT
    #         elif (int(online) > 0):
    #             payment_method = Transaction.ONLINE
    #         else:
    #             payment_method = Transaction.CASH

    #         # Create a new transaction instance
    #         transaction = Transaction.objects.create(
    #             session=session,
    #             total_cost=total_cost,
    #             payment_method=payment_method,
    #             unpaid_amount=unpaid_amount,
    #             amount_paid_cash=int(cash),
    #             amount_paid_online=int(online),
    #             payment_status=Transaction.FULLY_PAID if unpaid_amount == 0 else Transaction.UNPAID
    #         )

    #         transaction.save()

    #         # Update customer debt if transaction is unpaid
    #         if unpaid_amount > 0:
    #             customer.debt += int(unpaid_amount)
    #             customer.save()

    #         # Handle session type specific logic
    #         if session.session_type in ['PS5', 'PS4']:
    #             # Get tokens spent and saved
    #             tokens_spent = int(tokens_spent)
    #             tokens_saved = int(tokens_saved)

    #             # Update customer's tokens_spent and tokens_saved
    #             if session.session_type == 'PS5':
    #                 customer.ps5_tokens -= tokens_spent
    #                 customer.ps5_tokens += tokens_saved
    #             elif session.session_type == 'PS4':
    #                 customer.ps4_tokens -= tokens_spent
    #                 customer.ps4_tokens += tokens_saved

    #             customer.save()
    #         return Response({'message': 'Session ended'}, status=status.HTTP_200_OK)
    #     except Session.DoesNotExist:
    #         return Response({'message': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    def update(self, request, pk):
        try:
            session = Session.objects.get(pk=pk)
            customer = session.customer

            actual_duration = request.data.get('actual_duration')
            planned_duration = request.data.get('planned_duration')
            tokens_saved = request.data.get('tokens_saved', 0)
            tokens_spent = request.data.get('tokens_spent', 0)
            amount = request.data.get('amount', 0)
            online = request.data.get('online', 0) or 0
            cash = request.data.get('cash', 0) or 0

            session.actual_duration = actual_duration
            session.planned_duration = planned_duration
            session.save()

            try:
                total_cost = int(amount)
                amount_paid = int(online) + int(cash)
            except ValueError:
                return Response({'error': 'Invalid payment values'}, status=status.HTTP_400_BAD_REQUEST)

            unpaid_amount = max(total_cost - amount_paid, 0)

            if (int(cash) > 0) and (int(online) > 0):
                payment_method = Transaction.SPLIT
            elif (int(online) > 0):
                payment_method = Transaction.ONLINE
            else:
                payment_method = Transaction.CASH

            # Create a new transaction instance
            transaction = Transaction.objects.create(
                session=session,
                total_cost=total_cost,
                payment_method=payment_method,
                unpaid_amount=unpaid_amount,
                amount_paid_cash=int(cash),
                amount_paid_online=int(online),
                payment_status=Transaction.FULLY_PAID if unpaid_amount == 0 else Transaction.UNPAID
            )

            transaction.save()

            # Update customer debt if transaction is unpaid
            if unpaid_amount > 0:
                customer.debt += int(unpaid_amount)
                customer.save()

            # Handle session type specific logic
            if session.session_type in ['PS5', 'PS4']:
                # Get tokens spent and saved
                tokens_spent = int(tokens_spent)
                tokens_saved = int(tokens_saved)

                # Update customer's tokens_spent and tokens_saved
                if session.session_type == 'PS5':
                    customer.ps5_tokens -= tokens_spent
                    customer.ps5_tokens += tokens_saved
                elif session.session_type == 'PS4':
                    customer.ps4_tokens -= tokens_spent
                    customer.ps4_tokens += tokens_saved

                customer.save()
            return Response({'message': 'Session ended'}, status=status.HTTP_200_OK)
        except Session.DoesNotExist:
            return Response({'message': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)

