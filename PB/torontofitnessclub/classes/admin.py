from django.contrib import admin
from django.utils import timezone
from .models import Class, ClassKeyword, ClassOccurrence, ClassOccurrenceOverride
import nested_admin

class ClassKeywordInline(nested_admin.NestedTabularInline):
    model = ClassKeyword

class ClassOccurrenceOverrideInline(nested_admin.NestedTabularInline):
    model = ClassOccurrenceOverride
    extra = 0

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(start__gte=timezone.now())

class ClassOccurrenceInline(nested_admin.NestedTabularInline):
    model = ClassOccurrence
    extra = 1
    inlines = [ClassOccurrenceOverrideInline]

class ClassAdmin(nested_admin.NestedModelAdmin):
    inlines = [ClassKeywordInline, ClassOccurrenceInline]
    list_display = ('name', 'studio')

admin.site.register(Class, ClassAdmin)