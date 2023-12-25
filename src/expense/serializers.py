from rest_framework import serializers
from .models import Expense, Passbook

class ExpenseSerializer(serializers.ModelSerializer):
    """
        This serializer is responsible for converting Expense model instances
        to JSON format and vice versa. It specifies the fields to be included
        in the serialized representation and defines read-only fields.
    """
    class Meta:
        model = Expense
        fields = ('id', 'user', 'total_amount_spend', 'split_type')
        read_only_fields = ('id', 'user')  # 'id' and 'user' are read-only fields

class PassbookSerializer(serializers.ModelSerializer):
    """
        This serializer is responsible for converting Passbook model instances
        to JSON format and vice versa. It includes all the fields required for
        Passbook model instance.
    """
    class Meta:
        model = Passbook
        fields = '__all__'

class ExactDataSplitSerializer(serializers.Serializer):
    """
        This serializer is used to check the data being sent by frontend 
        for exact data split pattern
    """
    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class PercentageDictSerializer(serializers.Serializer):
    """
        This serializer is used to check the data being sent by frontend 
        for percentage data split pattern
    """
    user_id = serializers.IntegerField()
    percentage = serializers.IntegerField()