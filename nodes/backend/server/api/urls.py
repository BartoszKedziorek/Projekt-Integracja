from django.urls import path
from .views import UnemploymentAPIView, PopulationAPIView, InternetAPIView, ListCountryApiView, DetailCountryApiView, ExtremeUnemploymentCountryApiView, \
    ExtremePopulationCountryApiView, ExtremeInternetCountryApiView

app_name = 'api'

urlpatterns = [
    path('unemployment', UnemploymentAPIView.as_view(), name='unempl'),
    path('population',PopulationAPIView.as_view(), name="popul"),
    path('internet', InternetAPIView.as_view(), name="inter"),
    path('country', ListCountryApiView.as_view(), name="country_list"),
    path('country/<slug:code>', DetailCountryApiView.as_view(), name="country_detail"),
    path('unemployment/extreme', ExtremeUnemploymentCountryApiView.as_view(), name='extreme_unemployment'),
    path('population/extreme', ExtremePopulationCountryApiView.as_view(), name='extreme_population'),
    path('internet/extreme', ExtremeInternetCountryApiView.as_view(), name='extreme_internet'),
]
