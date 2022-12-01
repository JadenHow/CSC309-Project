from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django_google_maps import fields as map_fields

class Studio(models.Model):
    name = models.CharField(max_length=255)
    address = map_fields.AddressField(max_length=255, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=6, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.name

class StudioAmenity(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return f'{self.type} ({self.quantity})'

class StudioImage(models.Model):
    image = models.ImageField()
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    studio = models.ForeignKey(Studio, related_name='images', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return self.alt_text or self.image.name