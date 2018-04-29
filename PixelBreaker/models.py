from django.db import models

# Create your models here.

class ImageDetails(models.Model) :
    image = models.FileField(upload_to='images/cover_photos/', blank=True, null=True)