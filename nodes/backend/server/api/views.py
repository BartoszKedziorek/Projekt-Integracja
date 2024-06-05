from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PopulationSerializer, UnemploymentSerializer, InternetSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Unemployment, Population, Internet
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers
from django.db.models import Model

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

