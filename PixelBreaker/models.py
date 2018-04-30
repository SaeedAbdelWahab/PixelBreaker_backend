from django.db import models

# Create your models here.

class ImageDetails(models.Model) :
    number= models.IntegerField()
    image = models.FileField(upload_to='images/MeterReadings/', blank=True, null=True)
    date = models.DateField(auto_now=True)
    reading = models.CharField(max_length=50,blank=True,null=True)