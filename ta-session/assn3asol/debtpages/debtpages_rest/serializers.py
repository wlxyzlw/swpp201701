from rest_framework import serializers
from debtpages_rest.models import Debt
from django.contrib.auth.models import User

class DebtSerializer(serializers.ModelSerializer):
    borrower = serializers.ReadOnlyField(source='borrower.id')
    class Meta:
        model = Debt
        fields = ('id', 'created', 'amount', 'borrower', 'lender')

class DebtSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ('id', 'created', 'amount', 'borrower', 'lender')

class UserSerializer(serializers.ModelSerializer):
    debts_as_borrower = serializers.PrimaryKeyRelatedField(many=True, queryset=Debt.objects.all())
    debts_as_lender = serializers.PrimaryKeyRelatedField(many=True, queryset=Debt.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'debts_as_borrower', 'debts_as_lender')

class UserSumSerializer(serializers.BaseSerializer):
    def to_representation(self, obj):
        borrowed_money = 0
        lended_money = 0
        for debt in obj.debts_as_borrower.all():
            borrowed_money = borrowed_money + debt.amount
        for debt in obj.debts_as_lender.all():
            lended_money = lended_money + debt.amount
        return {
            "id":obj.id,
            "username":obj.username,
            "borrowed_money":borrowed_money,
            "lended_money":lended_money
        }
    debts_as_borrower = serializers.PrimaryKeyRelatedField(many=True, queryset=Debt.objects.all())
    debts_as_lender = serializers.PrimaryKeyRelatedField(many=True, queryset=Debt.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'debts_as_borrower', 'debts_as_lender')
