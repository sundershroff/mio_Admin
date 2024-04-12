from django.db import models

# Create your models here.
class comission_Editing(models.Model):
    per_km = models.IntegerField(null = True)
    incentive = models.IntegerField(null = True)

class business_commision(models.Model):
    commission =models.TextField(null=True)
    gst = models.TextField(null=True)