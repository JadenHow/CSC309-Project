from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import serializers, filters
from .models import Studio, StudioImage, StudioAmenity
from geopy import distance
import requests
from django.conf import settings
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ('id', 'name', 'address', 'geolocation', 'postal_code', 'phone_number', 'km_distance')

    km_distance = serializers.SerializerMethodField()
    def get_km_distance(self, studio):
        if not hasattr(studio, 'distance'):
            return None
        return round(studio.distance.km, 1)

class StudioDetailSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = ('id', 'name', 'address', 'geolocation', 'postal_code', 'phone_number', 'images', 'amenities', 'google_maps_url')

    images = serializers.SerializerMethodField()
    def get_images(self, obj):
        request = self.context.get('request')
        images = StudioImage.objects.filter(studio=obj)
        
        return [{'image': request.build_absolute_uri(image.image.url), 'alt_text': image.alt_text} for image in images]

    amenities = serializers.SerializerMethodField()
    def get_amenities(self, studio):
        return StudioAmenity.objects.filter(studio=studio).values('type', 'quantity')

    google_maps_url = serializers.SerializerMethodField()
    def get_google_maps_url(self, studio):
        return f'https://www.google.com/maps/dir/?api=1&destination={studio.geolocation}'

class StudioListView(ListAPIView):
    """
    List of all studios.
    """
    serializer_class = StudioSerializer
    search_fields = ['name', 'studioamenity__type', 'classes__name', 'classes__coach']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        queryset = Studio.objects.all()
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        postal_code = self.request.query_params.get('postal_code', None)

        point = None
        if latitude and longitude:
            point = (float(latitude), float(longitude))
        elif postal_code:
            response = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params={'address': postal_code, 'key': settings.GOOGLE_MAPS_API_KEY}).json()
            if response['status'] == 'OK':
                location = response['results'][0]['geometry']['location']
                point = (location['lat'], location['lng'])

        if point:
            for studio in queryset:
                studio.distance = distance.geodesic(point, (studio.geolocation.lat, studio.geolocation.lon))
            queryset = sorted(queryset, key=lambda studio: studio.distance)

        return queryset
    
    # lat_openapi = openapi.Parameter('latitude', openapi.IN_QUERY, description="If latitude and longitude are provided, the list in the response will be sorted by distance.", type=openapi.FORMAT_FLOAT)
    # long_openapi = openapi.Parameter('longitude', openapi.IN_QUERY, description="If latitude and longitude are provided, the list in the response will be sorted by distance.", type=openapi.FORMAT_FLOAT)
    # postal_code_openapi = openapi.Parameter('postal_code', openapi.IN_QUERY, description="If postal code is provided, the list in the response will be sorted by distance.", type=openapi.TYPE_STRING)

    # @swagger_auto_schema(manual_parameters=[lat_openapi, long_openapi, postal_code_openapi])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class StudioDetailView(RetrieveAPIView):
    """
    Retrieves a single studio with extra detail like its images, amenities, and more.
    """
    queryset = Studio.objects.all()
    serializer_class = StudioDetailSerialzier