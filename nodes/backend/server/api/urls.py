from django.urls import path
from .views import UnemploymentAPIView, PopulationAPIView

app_name = 'api'

urlpatterns = [
    path('unemployment', UnemploymentAPIView.as_view(), name='unempl'),
    path('population',PopulationAPIView.as_view(), name="popul")
]
