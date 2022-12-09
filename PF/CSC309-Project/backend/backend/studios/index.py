from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Studio, StudioAmenities
from classes.models import Class

@register(Studio)
class StudioIndex(AlgoliaIndex):
    fields = [
        'name',
        'phone_number',
        'address',
        'postal_code',
        'latitude',
        'longitude',
    ]
    settings = {
        'searchableAttributes': ['name']
    }

@register(StudioAmenities)
class StudioAmenitiesIndex(AlgoliaIndex):
    fields = [
        'studio',
        'type',
        'quantity',
    ]
    settings = {
        'searchableAttributes': ['type']
    }

@register(Class)
class ClassIndex(AlgoliaIndex):
    fields = [
        'studio',
        'name',
        'description',
        'coach',
        'keywords',
        'capacity',
        'start_date',
        'start_time',
        'end_time',
        'end_recursion',
        'cancelled',
    ]
    settings = {
        'searchableAttributes': ['name', 'coach']
    }