from rest_framework import serializers
from .models import Studio, StudioImages, StudioAmenities
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.reverse import reverse

class StudioAmenityInlineSerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True)
    quantity = serializers.CharField(read_only=True)

class StudioAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioAmenities
        fields = [
            'studio',
            'type',
            'quantity'
        ]

class StudioImageInlineSerializer(serializers.Serializer):
    image = serializers.FileField(read_only = True)

class StudioImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudioImages
        fields = [
            'studio',
            'image'
        ]

class StudioSerializer(serializers.ModelSerializer):
    amenities = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
            view_name='studios:studio-detail',
            lookup_field='pk',
            read_only=True
    )
    parser_classes = (MultiPartParser, FormParser)
    class Meta:
        model = Studio
        fields = [
            'pk',
            'owner',
            'name',
            'phone_number',
            'address',
            'postal_code',
            'latitude',
            'longitude',
            'url',
            'images',
            'amenities'
        ]

    def create(self, validated_data):
        new_studio = Studio.objects.create(**validated_data)
        return new_studio.pk
    
    def get_images(self, obj):
        studio = obj
        queryset = StudioImages.objects.all().filter(studio = studio)
        return StudioImageInlineSerializer(queryset, many=True).data
    
    def get_amenities(self, obj):
        studio = obj
        queryset = StudioAmenities.objects.all().filter(studio = studio)
        return StudioAmenityInlineSerializer(queryset, many=True).data
