from rest_framework import serializers
from .models import ExchangeRates


class ExchangeRatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = '__all__'


