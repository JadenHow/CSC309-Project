from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import ClassInstances

@register(ClassInstances)
class ClassInstancesIndex(AlgoliaIndex):
    should_index = 'is_not_cancelled'
    fields = [
        'studio',
        'name',
        'description',
        'coach',
        'keywords',
        'capacity',
        'currently_enrolled',
        'class_date',
        'class_date_timestamp',
        'start_time',
        'start_time_timestamp',
        'end_time',
    ]
    settings = {
        'searchableAttributes': ['name', 'coach', 'class_date_timestamp', 'start_time_timestamp'],
        'attributesForFaceting': ['studio']
    }
