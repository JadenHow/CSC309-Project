from django.contrib import admin
from .models import Studio, StudioImages, StudioAmenities

# Register your models here.
admin.site.register(Studio)
admin.site.register(StudioImages)
admin.site.register(StudioAmenities)