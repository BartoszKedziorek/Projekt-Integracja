from rest_framework import serializers
from .models import Unemployment, Population, Internet
from rest_framework.validators import ValidationError


class PopulationSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    value = serializers.IntegerField()

    class Meta:
        model = Population
        fields = ['year', 'value']


class UnemploymentSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    value = serializers.DecimalField(max_digits=6, decimal_places=3,coerce_to_string=False)

    class Meta:
        model = Unemployment
        fields = ['year', 'value']
    

class InternetSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField()
    cellularsubscription = serializers.FloatField()
    internetuserspercent = serializers.FloatField()
    internetusersnumber = serializers.IntegerField()
    broadbandsubscription = serializers.FloatField()

    class Meta:
        model = Internet
        fields = ['year', 'cellularsubscription',
                   'internetuserspercent', 'internetusersnumber',
                    'broadbandsubscription' ]