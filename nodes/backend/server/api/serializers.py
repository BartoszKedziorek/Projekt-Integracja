from rest_framework import serializers
from .models import Unemployment, Country
from rest_framework.validators import ValidationError


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["code", "name"]


class UnemploymentSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    value = serializers.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        model = Unemployment
        fields = ['year', 'value']