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
        self.internetUrl = reverse('api:inter')
        country = Country.objects.create(name='Brazil', code='BRA')
        self.testUnemplObjects = []
        for year, value in [(2014, 10.234), (2015, 9.024), (2016, 6.789)]:
            self.testUnemplObjects.append(
                Unemployment.objects.create(year=year, value=value, country=country))
        
        self.testPopulationObjects = []
        for year, value in [(2014, 12331), (2015, 32131), (2016, 42141)]:
            self.testPopulationObjects.append(
                Population.objects.create(year=year, value=value, country=country))
        
        self.testInternetObjects = []
        for year, cellularsubscription, internetuserspercent, internetusersnumber, broadbandsubscription \
        in [(2014,138.4511871,54.5510025,110989278,11.82082748),
            (2015,126.0879593,58.32795334,119682082,12.46259022),
            (2016,118.3855972,60.87253952,125920682,13.02890015)]:
            self.testInternetObjects.append(
                Internet.objects.create(year=year, cellularsubscription=cellularsubscription,
                                        internetusersnumber=internetusersnumber,
                                          internetuserspercent=internetuserspercent,
                                          broadbandsubscription=broadbandsubscription,
                                          country=country)
            )
        
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
            self.assertEqual(record["year"], self.testPopulationObjects[iter].year)
            self.assertAlmostEqual(record["value"], self.testPopulationObjects[iter].value)

    def test_population_missing_param(self):
        resp = self.client.get(self.populUrl + '?year_end=2014&year_start=2016') 
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


    # INTERNET TEST
    def test_internet_valid_resp_code(self):
        resp = self.client.get(self.internetUrl + "?year_start=2014&year_end=2016&code=BRA")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_internet_valid_resp_body(self):
        resp = self.client.get(self.internetUrl + "?year_start=2014&year_end=2016&code=BRA")
        resp_body = resp.json()

        self.assertEqual(resp_body["code"], "BRA")
        for iter, record in enumerate(resp_body["values"]):
            self.assertEqual(record["year"], self.testInternetObjects[iter].year)
            self.assertAlmostEqual(record["cellularsubscription"], self.testInternetObjects[iter].cellularsubscription)
            self.assertAlmostEqual(record["internetusersnumber"], self.testInternetObjects[iter].internetusersnumber)
            self.assertAlmostEqual(record["internetuserspercent"], self.testInternetObjects[iter].internetuserspercent)
            self.assertAlmostEqual(record["broadbandsubscription"], self.testInternetObjects[iter].broadbandsubscription)

    def test_internet_missing_param(self):
        resp = self.client.get(self.internetUrl + '?year_end=2014&year_start=2016') 
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    

