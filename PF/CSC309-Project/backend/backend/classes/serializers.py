from rest_framework import serializers
from .models import Class, ClassInstances

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = [
            'pk',
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
            'cancelled'
        ]

    def create(self, validated_data):
        new_class = Class.objects.create(**validated_data)
        return new_class

class ClassInstancesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassInstances
        fields = [
            'pk',
            'studio',
            'parent_class',
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
            'cancelled'
        ]
