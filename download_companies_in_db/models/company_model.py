from django.db import models

class CompanyModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    data = models.JSONField()