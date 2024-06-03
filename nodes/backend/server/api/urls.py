from django.urls import path
from .views import UnemploymentAPIView

app_name = 'api'

urlpatterns = [
    path('unemployment', UnemploymentAPIView.as_view(), name='unempl'),
]
