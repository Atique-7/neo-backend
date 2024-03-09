from rest_framework import serializers
from transactions.models import Transaction
from session.models import Session

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    session = SessionSerializer()  # Include the SessionSerializer here

    class Meta:
        model = Transaction
        fields = '__all__'