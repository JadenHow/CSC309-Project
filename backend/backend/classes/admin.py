from django.contrib import admin
from .models import Class, ClassInstances
from studios.models import Studio
from classes.serializers import ClassInstancesSerializer, ClassSerializer
from datetime import timedelta
import datetime
import time
from rest_framework.response import Response

# Register your models here.

class ClassAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change) -> None:
        studio_id = form.cleaned_data['studio'].pk

        if not change:
            if Studio.objects.filter(pk=studio_id).exists():
                # 'studio',
                obj.name = form.cleaned_data.get("name")
                obj.description = form.cleaned_data.get("description")
                obj.coach = form.cleaned_data.get("coach")
                obj.keywords = form.cleaned_data.get("keywords")
                obj.capacity = form.cleaned_data.get("capacity")
                obj.start_date = form.cleaned_data.get("start_date")
                obj.start_time = form.cleaned_data.get("start_time")
                obj.end_time = form.cleaned_data.get("end_time")
                obj.end_recursion = form.cleaned_data.get("end_recursion")

                super(ClassAdmin, self).save_model(request, obj, form, change)

                curr_date = form.cleaned_data.get("start_date")
                end = form.cleaned_data.get("end_recursion")

                while curr_date <= end:
                    curr_date_list = str(curr_date).split('-')
                    start_time_list = str(obj.start_time).split(':')
                    start_datetime = datetime.datetime(int(curr_date_list[0]), int(curr_date_list[1]), int(curr_date_list[2]), int(start_time_list[0]), int(start_time_list[1]))
                    start_datetime_unix = time.mktime(start_datetime.timetuple())
                        
                    start_time_timestamp = str(obj.start_time).split(':')
                    start_time_timestamp = start_time_timestamp[0] + start_time_timestamp[1] + start_time_timestamp[2]

                    instance_data = {
                        'studio': studio_id,
                        'parent_class': obj.pk,
                        'name': form.cleaned_data.get("name"),
                        'description': form.cleaned_data.get("description"),
                        'coach': form.cleaned_data.get("coach"),
                        'keywords': form.cleaned_data.get("keywords"),
                        'capacity': form.cleaned_data.get("capacity"),
                        'class_date': curr_date,
                        'class_date_timestamp': start_datetime_unix,
                        'start_time': form.cleaned_data.get("start_time"),
                        'start_time_timestamp' : start_time_timestamp,
                        'end_time': form.cleaned_data.get("end_time")
                    }

                    instance_serializer = ClassInstancesSerializer(data=instance_data)
                    if instance_serializer.is_valid(raise_exception=True):
                        instance_serializer.save()

                    curr_date += timedelta(days=7)
        else:
            for field in form.changed_data:
                # print(field)
                setattr(obj, field, form.cleaned_data.get(field))
                obj.save()

            # update the class instances
            queryset = ClassInstances.objects.all().filter(parent_class = obj.pk)

            for class_instance in queryset:
                for field in form.changed_data:
                    # print(field)
                    setattr(class_instance, field, form.cleaned_data.get(field))

                    if field == 'start_time':
                        start_time_timestamp_edited = str(obj.start_time).split(':')
                        start_time_timestamp_edited = start_time_timestamp_edited[0] + start_time_timestamp_edited[1] + start_time_timestamp_edited[2]
                        setattr(class_instance, 'start_time_timestamp', start_time_timestamp_edited)

                    class_instance.save()
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('start_date', 'end_recursion')
        return self.readonly_fields
   
   
class ClassInstancesAdmin(admin.ModelAdmin):
    exclude = ['class_date_timestamp', 'start_time_timestamp']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('studio', 'parent_class', 'name', 'description', 'coach', 'keywords', 'capacity', 'currently_enrolled', 'class_date', 'start_time', 'end_time')
        return self.readonly_fields

admin.site.register(ClassInstances, ClassInstancesAdmin)
# admin.site.register(ClassInstances)
admin.site.register(Class, ClassAdmin)
