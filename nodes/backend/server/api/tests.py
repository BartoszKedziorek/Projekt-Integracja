from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import path, include, reverse
from django.contrib.auth.models import User
from .models import Country, Unemployment, Population, Internet 


# Create your tests here.

class UsersTests(APITestCase):
    url_patterns = [
        path('', include('api.urls'))
    ]

    def setUp(self):
        self.unemplUrl = reverse('api:unempl')
        self.populUrl = reverse('api:popul')
        country = Country.objects.create(name='Brazil', code='BRA')
        self.testUnemplObjects = []
        for year, value in [(2014, 10.234), (2015, 9.024), (2016, 6.789)]:
            self.testUnemplObjects.append(
                Unemployment.objects.create(year=year, value=value, country=country))
            
    # UNEMPLOYMENT TEST
    def test_unemployment_valid_resp_code(self):
        resp = self.client.get(self.unemplUrl + "?year_start=2014&year_end=2016&code=BRA")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_unemployment_valid_resp_body(self):
        resp = self.client.get(self.unemplUrl + "?year_start=2014&year_end=2016&code=BRA")
        resp_body = resp.json()

        self.assertEqual(resp_body["code"], "BRA")
        for iter, record in enumerate(resp_body["values"]):
            self.assertEqual(record["year"], self.testUnemplObjects[iter].year)
            self.assertAlmostEqual(record["value"], self.testUnemplObjects[iter].value)

    def test_unemployment_missing_param(self):
        resp = self.client.get(self.unemplUrl + '?year_end=2014&year_start=2016') 
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)



    # POPULATION TEST
    def test_population_valid_resp_code(self):
        resp = self.client.get(self.populUrl + "?year_start=2014&year_end=2016&code=BRA")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_population_valid_resp_body(self):
        resp = self.client.get(self.populUrl + "?year_start=2014&year_end=2016&code=BRA")
        resp_body = resp.json()

        self.assertEqual(resp_body["code"], "BRA")
        for iter, record in enumerate(resp_body["values"]):
            self.assertEqual(record["year"], self.testUnemplObjects[iter].year)
            self.assertAlmostEqual(record["value"], self.testUnemplObjects[iter].value)

    def test_population_missing_param(self):
        resp = self.client.get(self.populUrl + '?year_end=2014&year_start=2016') 
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    

