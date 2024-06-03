from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UnemploymentSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Unemployment


class UnemploymentAPIView(APIView):
    def get(self, request, *args, **kwargs):
        required_params = ['year_start', 'year_end', 'value']
        # check if quey container required parameters
        for param in required_params:
            if param not in request.GET.keys():
                return Response({
                    "message": "query parameter: {} is missing".format(param) 
                },
                status=status.HTTP_400_BAD_REQUEST) 
        
        unemployments = Unemployment.objects.filter(country__code=request.GET['code']) \
                        .filter(year__gte=request.GET['year_start']) \
                        .filter(year__gte=request.GET['year_end'])

        serializer = UnemploymentSerializer(unemployments, many=True)
        response = {
            "code": request.GET['code'],
            "values": serializer.data
        }
        
        return Response(response, status=status.HTTP_200_OK)


        


