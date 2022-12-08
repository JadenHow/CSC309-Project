from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from studios.models import Studio
from classes.models import ClassInstances        
from classes.serializers import ClassInstancesSerializer
from rest_framework import generics, permissions
from knox.auth import TokenAuthentication
import datetime
from users.models import Enrolled, RegisterUser
from subscriptions.models import SubscriptionInstance
from users.serializers import EnrolledSerializer
from . import client
from rest_framework.pagination import LimitOffsetPagination


class EnrolAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, studio_id, class_id):
        # /studios/classes/<classid>/enrol
        # studio = get_object_or_404(Studio, pk=studio_id)
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        if not get_object_or_404(RegisterUser, user=request.user.id).subscribed:
            return Response({"msg" : "not subscribed"}, status=404)

        if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
            return Response({"msg" : "subscription will be expired before the class, please enrol after your subscription is renewed or subscribe to a longer subscription"}, status=404)

        # print(request.user)
        curr_time = datetime.datetime.now().time()
        today = datetime.date.today()

        # can't already be enrolled
        if Enrolled.objects.filter(class_instance = class_id, user = request.user.id).exists():
            print(Enrolled.objects.filter(class_instance = class_id, user = request.user.id))
            return Response({
                "msg": "Already enrolled" 
            }, status=404)


        if class_instance.currently_enrolled < class_instance.capacity and class_instance.class_date >= today:
            if class_instance.class_date == today and class_instance.start_time <= curr_time:
                return Response({
                    "msg": "Class has already passed" 
                    })

            data = {
                'user': request.user.id,
                'class_instance': class_id
            }

            serializer = EnrolledSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                class_instance.currently_enrolled += 1
                class_instance.save()

            return Response({
                "msg": "Successfully Enrolled" 
            }, status=200)
        else:
            return Response({"msg" : "Doens't work"}, status=404)


class DropAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, studio_id, class_id):
        if not ClassInstances.objects.filter(parent_class=class_id, studio=studio_id).exists:
            return Response({"msg" : "Class doesn't exist"}, status=404)

        print(class_id, request.user.id)
        enrolled_instance = Enrolled.objects.filter(class_instance=class_id, user = request.user.id)
        print(enrolled_instance)
        if enrolled_instance.exists():
            enrolled_instance.delete()

            # subract currently enrolled
            class_instance = get_object_or_404(ClassInstances, pk=class_id)
            class_instance.currently_enrolled -= 1
            class_instance.save() 

            return Response({
                "msg": "Successfully dropped" 
            }, status=200)
        else: 
            return Response({
                "msg": "Not enrolled" 
            }, status=404)


class ClassSearchAPIView(generics.ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = ClassInstancesSerializer
    queryset = ''
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        start = request.GET.get('start') or None
        end = request.GET.get('end') or None
        starttime = request.GET.get('starttime') or None
        endtime = request.GET.get('endtime') or None

        results = client.perform_search(query, start=start, end=end, starttime=starttime, endtime=endtime)
        # print(results['hits'])
        page = self.paginate_queryset(results['hits'])
        return self.get_paginated_response(page)

class_search_view = ClassSearchAPIView.as_view()

class EnrolMultipleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes= [permissions.IsAuthenticated]

    def post(self, request, studio_id, class_id):
        # studio = get_object_or_404(Studio, pk=studio_id)
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        if not get_object_or_404(RegisterUser, user=request.user.id).subscribed:
            return Response({"msg" : "not subscribed"}, status=404)

        if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
            return Response({"msg" : "subscription will be expired before the class, please enrol after your subscription is renewed or subscribe to a longer subscription"}, status=404)

        curr_time = datetime.datetime.now().time()
        today = datetime.date.today()

        all_class_instances = ClassInstances.objects.filter(parent_class = class_instance.parent_class)

        for class_instance in all_class_instances:
            # Can't already be enrolled
            if Enrolled.objects.filter(class_instance = class_instance.pk, user = request.user.id).exists():
                continue
            if class_instance.currently_enrolled < class_instance.capacity and class_instance.class_date >= today:
                if class_instance.class_date == today and class_instance.start_time <= curr_time:
                    continue
            if get_object_or_404(SubscriptionInstance, user=request.user.id).renewal_date < class_instance.class_date:
                continue
            
            data = {
                'user': request.user.id,
                'class_instance': class_instance.pk
            }

            serializer = EnrolledSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                class_instance.currently_enrolled += 1
                class_instance.save()

        return Response({
            "msg": "Successfully enrolled to all future occurrences" 
        }, status=200)

class DropMultipleAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, studio_id, class_id):
        if not ClassInstances.objects.filter(parent_class=class_id, studio=studio_id).exists:
            return Response({"msg" : "Class doesn't exist"}, status=404)
        
        class_instance = get_object_or_404(ClassInstances, pk=class_id)

        all_class_instances = ClassInstances.objects.filter(parent_class = class_instance.parent_class)

        for class_instance in all_class_instances:
            enrolled_instance = Enrolled.objects.filter(class_instance=class_instance.pk, user = request.user.id)
        
            if enrolled_instance.exists():
                enrolled_instance.delete()

                # subract currently enrolled
                class_instance_object = get_object_or_404(ClassInstances, pk=class_instance.pk)
                class_instance_object.currently_enrolled -= 1
                class_instance_object.save() 

        return Response({
            "msg": "Successfully dropped all future occurrences" 
        }, status=200)

# class CancelAllClasses(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, studio_id, class_id):

#         curr_studio = get_object_or_404(Studio, pk=studio_id)
#         if curr_studio.owner != request.user.id:
#             return Response({"msg" : "Permission denied"}, status=403)

#         curr_class = get_object_or_404(Class, pk=class_id, studio = studio_id)
#         curr_class.cancelled = True
#         curr_class.save()

#         queryset = ClassInstances.objects.all().filter(parent_class = curr_class.pk)

#         for obj in queryset:
#             obj.cancelled = True
#             obj.save()

#         return Response({"msg" : "Successfully cancelled"}, status=200)


# class UpdateClassAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def patch(self, request, studio_id, class_id):
        
#         curr_studio = get_object_or_404(Studio, pk=studio_id)
#         # print(curr_studio.owner)
#         # print(request.user)

#         if curr_studio.owner != request.user.id:
#             return Response({"msg" : "Permission denied"}, status=403)

#         data = request.data

#         curr_class = get_object_or_404(Class, pk=class_id)
#         serializer = ClassSerializer(curr_class, data = data, partial = True)

#         if serializer.is_valid():
#             serializer.save()

#             return Response({"msg" : "Successfully edited"}, status=200)


# Create your views here.
# class ClassCreateApiView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request, studio_id):
#         if Studio.objects.filter(pk=studio_id).exists():

#             studio = Studio.objects.get(pk=studio_id)
#             if studio.owner != request.user:
#                 return Response({"msg" : "Permission denied"}, status=403)

#             # 'studio',
#             name = request.data.get("name")
#             description = request.data.get("description")
#             coach = request.data.get("coach")
#             keywords = request.data.get("keywords")
#             capacity = request.data.get("capacity")
#             start_date = request.data.get("start_date")
#             start_time = request.data.get("start_time")
#             end_time = request.data.get("end_time")
#             end_recursion = request.data.get("end_recursion")

#             data = {
#                 'studio': studio_id,
#                 'name': name,
#                 'description': description,
#                 'coach': coach,
#                 'keywords': keywords,
#                 'capacity': capacity,
#                 'start_date': start_date,
#                 'start_time': start_time,
#                 'end_time': end_time,
#                 'end_recursion': end_recursion
#             }

#             serializer = ClassSerializer(data = data)
#             if serializer.is_valid(raise_exception=True):
#                 created_class = serializer.save()

#                 curr_date = created_class.start_date
#                 end = created_class.end_recursion

#                 while curr_date <= end:
#                     curr_date_list = str(curr_date).split('-')
#                     start_time_list = start_time.split(':')
#                     start_datetime = datetime.datetime(int(curr_date_list[0]), int(curr_date_list[1]), int(curr_date_list[2]), int(start_time_list[0]), int(start_time_list[1]))
#                     start_datetime_unix = time.mktime(start_datetime.timetuple())
                    
#                     start_time_timestamp = start_time.split(':')
#                     start_time_timestamp = start_time_timestamp[0] + start_time_timestamp[1] + start_time_timestamp[2]

#                     instance_data = {
#                         'studio': studio_id,
#                         'parent_class': created_class.pk,
#                         'name': name,
#                         'description': description,
#                         'coach': coach,
#                         'keywords': keywords,
#                         'capacity': capacity,
#                         'class_date': curr_date,
#                         'class_date_timestamp': start_datetime_unix,
#                         'start_time': start_time,
#                         'start_time_timestamp' : start_time_timestamp,
#                         'end_time': end_time,
#                     }

#                     instance_serializer = ClassInstancesSerializer(data=instance_data)
#                     if instance_serializer.is_valid(raise_exception=True):
#                         instance_serializer.save()

#                     curr_date += timedelta(days=7)

#                 return JsonResponse({
#                     "works": "works" 
#                 })
                    
#         return JsonResponse({
#                 "studio_id": "NOT REAL" 
#             })

