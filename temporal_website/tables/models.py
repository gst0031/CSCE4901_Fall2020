from django.db import models
#from django_pandas.managers import DataFrameManager

class excel(models.Model):
    cluster = models.IntegerField()
    terms = models.CharField(max_length=512)


