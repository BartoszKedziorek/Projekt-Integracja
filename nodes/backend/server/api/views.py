from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PopulationSerializer, UnemploymentSerializer, InternetSerializer, CountrySerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Unemployment, Population, Internet, Country
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers
from django.db.models import Model
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime
from django.db.models import Avg, Subquery

class GetValuesFromRangeMixin(APIView):
    model = Model
    serializer_class = serializers.Serializer

    def get(self, request, *args, **kwargs):
        required_params = ['year_start', 'year_end', 'code']
        # check if quey container required parameters
        for param in required_params:
            if param not in request.query_params.keys():
                return Response({
                    "message": "query parameter: {} is missing".format(param) 
                },
                status=status.HTTP_400_BAD_REQUEST) 
        
        unemployments = self.model.objects.filter(country__code=request.GET['code']) \
                        .filter(year__gte=request.GET['year_start']) \
                        .filter(year__lte=request.GET['year_end']) \
                        .order_by('year').values()

        serializer = self.serializer_class(unemployments, many=True)
        response = {
            "code": request.GET['code'],
            "values": serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)   


class UnemploymentAPIView(GetValuesFromRangeMixin):
    model = Unemployment
    serializer_class = UnemploymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
            parameters=[
                OpenApiParameter(name="year_start", type=int, required=True),
                OpenApiParameter(name="year_end", type=int, required=True),
                OpenApiParameter(name="code", type=str, description="Country code", required=True)
            ],
            responses={
                200: inline_serializer(
                    name=model.__name__+"ResponseSuccess",
                    fields={
                        "code": serializers.CharField(),
                        "values": inline_serializer(name=model.__name__+"ResponseValues",
                            fields={
                            "year": serializers.IntegerField(),
                            "value": serializers.DecimalField(max_digits=6, decimal_places=3, coerce_to_string=False)
                        }, many=True)
                    }
                ),
                400: inline_serializer(
                    name=model.__name__+"ResponseFailure",
                    fields={
                        "message": serializers.CharField()
                    }
                )
            }
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class PopulationAPIView(GetValuesFromRangeMixin):
    model = Population
    serializer_class = PopulationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
            parameters=[
                OpenApiParameter(name="year_start", type=int, required=True),
                OpenApiParameter(name="year_end", type=int, required=True),
                OpenApiParameter(name="code", type=str, description="Country code", required=True)
            ],
            responses={
                200: inline_serializer(
                    name=model.__name__+"ResponseSuccess",
                    fields={
                        "code": serializers.CharField(),
                        "values": inline_serializer(name=model.__name__+"ResponseValues",
                            fields={
                            "year": serializers.IntegerField(),
                            "value": serializers.IntegerField()
                        }, many=True)
                    }
                ),
                400: inline_serializer(
                    name=model.__name__+"ResponseFailure",
                    fields={
                        "message": serializers.CharField()
                    }
                )
            }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



class InternetAPIView(GetValuesFromRangeMixin):
    model = Internet
    serializer_class = InternetSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
            parameters=[
                OpenApiParameter(name="year_start", type=int, required=True),
                OpenApiParameter(name="year_end", type=int, required=True),
                OpenApiParameter(name="code", type=str, description="Country code", required=True)
            ],
            responses={
                200: inline_serializer(
                    name=model.__name__+"ResponseSuccess",
                    fields={
                        "code": serializers.CharField(),
                        "values": InternetSerializer(many=True)
                    }
                ),
                400: inline_serializer(
                    name=model.__name__+"ResponseFailure",
                    fields={
                        "message": serializers.CharField()
                    }
                )
            }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    

class ListCountryApiView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DetailCountryApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(responses={
        200: CountrySerializer,
        400: inline_serializer(
                    name="DetailCountryResponseFailure",
                    fields={
                        "message": serializers.CharField()
                    }
                )
    })
    def get(self, request, code, *args, **kwargs):
        country = get_object_or_404(Country, code=code)
        serializer = CountrySerializer(country)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ExtremeMixin(APIView):
    model = Model
    value_field = ''
    @extend_schema(
            parameters=[
                OpenApiParameter(name="years", type=int, required=True, description='how many last years'),
                OpenApiParameter(name="amount", type=int, required=True, description='number of results'),
                OpenApiParameter(name="extreme_type", type=str, description="'min' or 'max'", required=True)
            ],
            responses={
                200: inline_serializer(
                    name="ExtremeResponseSuccess",
                    fields={
                        'code':serializers.CharField(),
                        'name':serializers.CharField(),
                        'value':serializers.DecimalField(max_digits=6, decimal_places=3)
                    }, many=True
                ),
                400: inline_serializer(
                    name="ExtremeResponseFailure",
                    fields={
                        "message": serializers.CharField()
                    }
                )
            }
    )
    def get(self, request):
        required_params = ['years', 'amount', 'extreme_type']
        # check if quey container required parameters
        for param in required_params:
            if param not in request.query_params.keys():
                return Response({
                    "message": "query parameter: {} is missing".format(param) 
                },
                status=status.HTTP_400_BAD_REQUEST) 
            
        current_year = datetime.datetime.today().year
        query_year = current_year - int(request.GET['years'])

        avg_values = self.model.objects.filter(year__gte=query_year) \
            .values('country').annotate(avg=Avg(self.value_field)) \
            .exclude(country__code__in=('IBT','LMY','MIC','IBD','EAR', 'LMC','EAS','LTE','EAP','TEA'))
            #.order_by('-avg')[:request.GET['amount']]
        
        avg_values = [{
            'id': entry['country'],
            'avg': float(entry['avg']) if entry['avg'] is not None else None 
        }
        for entry in avg_values
        ]

        avg_values = list(filter(lambda x: x['avg'] is not None, avg_values))
        avg_values.sort(key=lambda x: x['avg'], reverse=True if request.GET['extreme_type'] == 'max' else False)
        avg_values = avg_values[:int(request.GET['amount'])]


        # Pobranie identyfikatorów krajów z listy średnich wartości
        highest_avg_countries = [{
            'code':Country.objects.get(id=entry['id']).code,
            'name':Country.objects.get(id=entry['id']).name,
            'value':entry['avg']
        }
        for entry in avg_values
        ]

        return Response(data=highest_avg_countries, status=status.HTTP_200_OK)

class ExtremeUnemploymentCountryApiView(ExtremeMixin):
    model = Unemployment
    value_field = 'value'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class ExtremePopulationCountryApiView(ExtremeMixin):
    model = Population
    value_field = 'value'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class ExtremeInternetCountryApiView(ExtremeMixin):
    model = Internet
    value_field = 'internetuserspercent'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]