from django.db import models

# Create your models here.
class Class(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        
    studio = models.ForeignKey('studios.Studio', on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=False, null=False)
    description = models.CharField(max_length=120, null=True)
    coach = models.CharField(max_length=120, null=True)
    keywords = models.CharField(max_length=120, null=True)
    capacity = models.PositiveIntegerField(default=0, blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    start_time = models.TimeField(blank=False, null=False)
    end_time = models.TimeField(blank=False, null=False)
    end_recursion = models.DateField(blank=False, null=False)
    cancelled = models.BooleanField(default=False, null=False)

class ClassInstances(models.Model):
    class Meta:
        verbose_name = 'Class Instance'
        verbose_name_plural = 'Class Instances'
    
    studio = models.ForeignKey('studios.Studio', on_delete=models.CASCADE)
    parent_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, blank=False, null=False)
    description = models.CharField(max_length=120, null=True)
    coach = models.CharField(max_length=120, null=True)
    keywords = models.CharField(max_length=120, null=True)
    capacity = models.PositiveIntegerField(default=0, blank=False, null=False)
    currently_enrolled = models.PositiveIntegerField(default=0, blank=False, null=False)
    class_date = models.DateField(blank=False, null=False)
    class_date_timestamp = models.IntegerField(blank=True, null=True)
    start_time = models.TimeField(blank=False, null=False)
    start_time_timestamp = models.IntegerField(blank=True, null=True)
    end_time = models.TimeField(blank=False, null=False)
    cancelled = models.BooleanField(default=False, null=False)
    
    def is_not_cancelled(self):
            return not self.cancelled
