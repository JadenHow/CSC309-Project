from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, filters
from .models import Class, RecurringAttendee, OneTimeAttendee, OneTimeNonAttendee
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import dateutil.parser
from django.contrib.auth.models import User
from django.db import IntegrityError
from collections import defaultdict
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSubscribed
# from drf_yasg import openapi
# from drf_yasg.utils import swagger_auto_schema

# from_openapi = openapi.Parameter('from', openapi.IN_QUERY, description="The date the returned schedule will begin from. If not specified, the current date and time is used.", type=openapi.FORMAT_DATETIME)
# to_openapi = openapi.Parameter('to', openapi.IN_QUERY, description="The date the returned schedule will end at. If not specified, one month from today is used.", type=openapi.FORMAT_DATETIME)

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', 'description', 'coach', 'total_capacity', 'available_capacity')
    
class StudioClassesView(ListAPIView):
    """
    List of all classes in studio {id}.
    """

    queryset = Class.objects.all()
    serializer_class = ClassSerializer

class ClassOccurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'start', 'end', 'available_capacity')
        model = Class

    id = serializers.SerializerMethodField()
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    available_capacity = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[2].id
    
    def get_start(self, obj):
        return obj[0]
    
    def get_end(self, obj):
        return obj[1]

    def get_available_capacity(self, obj):
        return obj[2].event.available_capacity_for_date(obj[0])

class StudioScheduleView(ListAPIView):
    """
    Schedule of all classes in studio {id}.
    """
    
    serializer_class = ClassOccurrenceSerializer
    search_fields = ['name', 'coach']
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        studio_id = self.kwargs.get('pk')
        classes = Class.objects.filter(studio=studio_id).all()
        return classes
    
    def get_serializer(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        query_params = self.request.query_params
        from_date = timezone.now()
        to_date = timezone.now() + relativedelta(months=+1)

        from_date_param = dateutil.parser.parse(query_params.get('from', None)) if query_params.get('from', None) else None
        if from_date_param:
            from_date = from_date_param
        to_date_param = dateutil.parser.parse(query_params.get('to', None)) if query_params.get('to', None) else None
        if to_date_param:
            to_date = to_date_param

        occurrences = list(queryset.all_occurrences(from_date=from_date, to_date=to_date))
        return ClassOccurrenceSerializer(occurrences, many=True)

    # @swagger_auto_schema(manual_parameters=[from_openapi, to_openapi])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class EnrolSerializer(serializers.Serializer):
    class_date = serializers.DateTimeField(required=False, help_text="If provided, enrols the user in the class on the given date. If not provided, enrols the user for every future occurrence of the class.")

class EnrolView(APIView):
    """
    Enrol in class {id}.
    """
    serializer_class = EnrolSerializer
    permission_classes = [IsAuthenticated, IsSubscribed]

    # @swagger_auto_schema(request_body=EnrolSerializer)
    def post(self, request, *args, **kwargs):
        class_id = self.kwargs.get('pk')
        serializer = EnrolSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        class_date = serializer.validated_data.get('class_date')
        user = self.request.user
        class_ = Class.objects.get(id=class_id)
        if class_date:
            if RecurringAttendee.objects.filter(class_key=class_, user=user, disenrol_date=None).exists() and not OneTimeNonAttendee.objects.filter(class_key=class_, user=user, class_date=class_date).exists():
                return Response({'error': 'User is already enrolled in this class.'}, status=400)

            if len(list(class_.all_occurrences(from_date=class_date, to_date=class_date))) == 0:
                return Response({'error': 'Class does not occur on this date.'}, status=400)
            if class_.available_capacity_for_date(class_date) > 0:
                if OneTimeNonAttendee.objects.filter(class_key=class_, user=user, class_date=class_date).exists():
                    OneTimeNonAttendee.objects.filter(class_key=class_, user=user, class_date=class_date).delete()
                else:
                    try:
                        OneTimeAttendee.objects.create(user=user, class_key=class_, class_date=class_date)
                    except IntegrityError:
                        return Response({'error': 'User is already enrolled in this class.'}, status=400)
            else:
                return Response({'error': 'Class is full.'}, status=400)
        else:
            if class_.available_capacity > 0:
                if RecurringAttendee.objects.filter(class_key=class_, user=user, disenrol_date=None).exists():
                    return Response({'error': 'User is already enrolled in this class.'}, status=400)
                RecurringAttendee.objects.create(user=user, class_key=class_, enrol_date=timezone.now())
                OneTimeAttendee.objects.filter(class_key=class_, user=user, class_date__gte=timezone.now()).delete()
            else:
                return Response({'error': 'Class is full.'}, status=400)
        return Response({'success': 'User enrolled in class.'}, status=200)

class DisenrolSerializer(serializers.Serializer):
    class_date = serializers.DateTimeField(required=False, help_text="If provided, disenrols the user from the class on the given date. If not provided, disenrols the user from every future occurrence of the class.")

class DisenrolView(APIView):
    """
    Disenrol from class {id}.
    """
    serializer_class = DisenrolSerializer
    permission_classes = [IsAuthenticated, IsSubscribed]

    # @swagger_auto_schema(request_body=DisenrolSerializer)
    def post(self, request, *args, **kwargs):
        class_id = self.kwargs.get('pk')
        serializer = DisenrolSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        class_date = serializer.validated_data.get('class_date')
        user = self.request.user
        class_ = Class.objects.get(id=class_id)

        if class_date:
            if class_date < timezone.now():
                return Response({'error': 'Class has already happened, cannot disenrol.'}, status=400)

            if len(list(class_.all_occurrences(from_date=class_date, to_date=class_date))) == 0:
                return Response({'error': 'Class does not occur on this date.'}, status=400)

            attendee = OneTimeAttendee.objects.filter(user=user, class_key=class_, class_date=class_date)
            if attendee.exists():
                attendee.delete()
            else:
                if RecurringAttendee.objects.filter(user=user, class_key=class_, disenrol_date=None).exists():
                    try:
                        OneTimeNonAttendee.objects.create(user=user, class_key=class_, class_date=class_date)
                        return Response({'success': 'User disenrolled from class.'}, status=200)
                    except IntegrityError:
                        return Response({'error': 'User is not enrolled in this class.'}, status=400)

                return Response({'error': 'User is not enrolled in this class.'}, status=400)
        else:
            try:
                attendee = RecurringAttendee.objects.get(user=user, class_key=class_, disenrol_date=None)
                attendee.disenrol_date = timezone.now()
                attendee.save()
            except RecurringAttendee.DoesNotExist:
                return Response({'error': 'User is not enrolled in this class.'}, status=400)

        return Response({'success': 'User disenrolled from class.'}, status=200)

class UserClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('classes', )

    classes = serializers.SerializerMethodField()
    def get_classes(self, user):
        user = self.context.get('request').user

        query_params = self.context.get('request').query_params

        from_date = timezone.now()
        to_date = timezone.now() + relativedelta(months=+1)

        from_date_param = dateutil.parser.parse(query_params.get('from', None)) if query_params.get('from', None) else None
        if from_date_param:
            from_date = from_date_param
        to_date_param = dateutil.parser.parse(query_params.get('to', None)) if query_params.get('to', None) else None
        if to_date_param:
            to_date = to_date_param

        classes_recurring = RecurringAttendee.objects.filter(user=user.id)
        classes_one_time = OneTimeAttendee.objects.filter(user=user.id)
        classes_non_one_time = OneTimeNonAttendee.objects.filter(user=user.id)

        classes = defaultdict(dict)

        for attendee in classes_recurring:
            for start_date, end_date, _ in attendee.class_key.all_occurrences(from_date=attendee.enrol_date, to_date=attendee.disenrol_date):
                if start_date < from_date or start_date > to_date:
                    continue
                classes[attendee.class_key.id].setdefault('occurrences', [])
                classes[attendee.class_key.id]['occurrences'].append(
                    {
                        'start': start_date,
                        'end': end_date
                    }
                )

        for attendee in classes_one_time:
            # TODO: standarize timezones
            if attendee.class_date < from_date or attendee.class_date > to_date:
                continue
            end_date = list(attendee.class_key.all_occurrences(from_date=attendee.class_date, to_date=attendee.class_date))[0][1]
            classes[attendee.class_key.id].setdefault('occurrences', [])
            classes[attendee.class_key.id]['occurrences'].append(
                {
                    'start': attendee.class_date,
                    'end': end_date
                }
            )

        for attendee in classes_non_one_time:
            if attendee.class_key.id not in classes:
                continue
            for occurrence in classes[attendee.class_key.id]['occurrences']:
                if occurrence['start'] == attendee.class_date:
                    classes[attendee.class_key.id]['occurrences'].remove(occurrence)
                    break
        
        for class_id in classes.keys():
            class_ = Class.objects.get(id=class_id)
            classes[class_id]['name'] = class_.name
            classes[class_id]['coach'] = class_.coach

        return classes

class UserClassScheduleView(RetrieveAPIView):
    """
    Get user's class schedule.
    """
    queryset = User.objects.all()
    serializer_class = UserClassScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # @swagger_auto_schema(manual_parameters=[from_openapi, to_openapi])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)