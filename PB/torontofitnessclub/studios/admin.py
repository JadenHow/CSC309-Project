from django.contrib import admin
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
import json

from .models import Studio, StudioImage, StudioAmenity

class StudioImageInline(admin.TabularInline):
    model = StudioImage

class StudioAmenityInline(admin.TabularInline):
    model = StudioAmenity

class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = [StudioImageInline, StudioAmenityInline]
    formfield_overrides = {
        map_fields.AddressField: {
            'widget': map_widgets.GoogleMapsAddressWidget(
                attrs={
                    'data-map-type': 'roadmap',
                    'data-autocomplete-options': json.dumps(
                        {
                            'types': ['geocode', 'establishment'],
                            'componentRestrictions': {'country': 'ca'},
                        }
                    )
                }
            )
        }
    }


admin.site.register(Studio, StudioAdmin)