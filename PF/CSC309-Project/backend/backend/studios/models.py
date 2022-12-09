from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Studio(models.Model):
    class Meta:
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=120, null=True)
    postal_code = models.CharField(max_length=120, null=True)

    # geographical_location
    latitude = models.DecimalField(max_digits=15, decimal_places=6, blank=False, null=False, 
    validators=[
        MaxValueValidator(90),
        MinValueValidator(-90)
    ])
    longitude = models.DecimalField(max_digits=15, decimal_places=6, blank=False, null=False, 
    validators=[
        MaxValueValidator(180),
        MinValueValidator(-180)
    ])

class StudioImages(models.Model):
    class Meta:
        verbose_name = 'Studio Image'
        verbose_name_plural = 'Studio Images'

    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True)

class StudioAmenities(models.Model):
    class Meta:
        verbose_name = 'Studio Amenity'
        verbose_name_plural = 'Studio Amenities'
    
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    type = models.CharField(max_length=120, null=True)
    quantity = models.IntegerField()
