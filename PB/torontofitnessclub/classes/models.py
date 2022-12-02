from django.db import models
from eventtools.models import BaseEvent, BaseOccurrence, default_naive
from studios.models import Studio
from dateutil.rrule import rruleset

class Class(BaseEvent):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    coach = models.CharField(max_length=255, blank=True, null=True)
    total_capacity = models.PositiveIntegerField(blank=True, null=True)
    studio = models.ForeignKey(Studio, related_name='classes', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def available_capacity(self):
        total_capacity = self.total_capacity if self.total_capacity else 0
        return total_capacity - RecurringAttendee.objects.filter(class_key=self.id, disenrol_date=None).count()

    def available_capacity_for_date(self, date):
        return self.available_capacity - OneTimeAttendee.objects.filter(class_key=self.id, class_date=date).count() + OneTimeNonAttendee.objects.filter(class_key=self.id, class_date=date).count()

    class Meta:
        verbose_name_plural = 'Classes'

    def __str__(self):
        return self.name

class RecurringAttendee(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class_key = models.ForeignKey(Class, related_name='recurring_attendees', on_delete=models.CASCADE)
    enrol_date = models.DateTimeField()
    disenrol_date = models.DateTimeField(blank=True, null=True)

class OneTimeAttendee(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class_key = models.ForeignKey(Class, related_name='one_time_attendees', on_delete=models.CASCADE)
    class_date = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'class_key', 'class_date')

class OneTimeNonAttendee(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    class_key = models.ForeignKey(Class, related_name='one_time_non_attendees', on_delete=models.CASCADE)
    class_date = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'class_key', 'class_date')

class ClassKeyword(models.Model):
    keyword = models.CharField(max_length=255)
    class_key = models.ForeignKey(Class, related_name='keywords', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

    def __str__(self):
        return self.keyword

class ClassOccurrence(BaseOccurrence):
    event = models.ForeignKey(Class, on_delete=models.CASCADE)

    def get_repeater(self):
        # From: https://github.com/gregplaysguitar/django-eventtools/issues/20#issuecomment-301910132
        rule = super().get_repeater()  # gets an rrule from parent method
        ruleset = rruleset()  # enables more sophisticated recurrence logic
        ruleset.rrule(rule)
        exclusions = ClassOccurrenceOverride.objects.filter(occurrence=self)
        for exclusion in exclusions:
            ruleset.exdate(default_naive(exclusion.start))  # remove occurrence
            if exclusion.modified_start:  # reschedule occurrence if defined
                ruleset.rdate(default_naive(exclusion.modified_start))
        return ruleset

    class Meta:
        verbose_name = 'Occurrence'
        verbose_name_plural = 'Occurrences'

class ClassOccurrenceOverride(models.Model):
    start = models.DateTimeField()
    modified_start = models.DateTimeField(blank=True, null=True)
    occurrence = models.ForeignKey(ClassOccurrence, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Override'
        verbose_name_plural = 'Overrides'

    def __str__(self):
        if self.modified_start:
            return f'{self.start} -> {self.modified_start}'
        else:
            return f'{self.start} -> CANCELLED'