from django.db import models

class Country(models.Model):
    name = models.CharField(unique=True, max_length=120)
    code = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'country'


class Internet(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    year = models.IntegerField()
    cellularsubscription = models.FloatField()
    internetuserspercent = models.FloatField()
    internetusersnumber = models.IntegerField()
    broadbandsubscription = models.FloatField()

    class Meta:
        db_table = 'internet'


class Population(models.Model):
    year = models.IntegerField()
    value = models.BigIntegerField(blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        db_table = 'population'


class Unemployment(models.Model):
    year = models.IntegerField()
    value = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        db_table = 'unemployment'