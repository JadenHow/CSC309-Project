from django.urls import path
from .views import StudioClassesView, StudioScheduleView, EnrolView, DisenrolView, UserClassScheduleView

urlpatterns = [
    path('<int:pk>/', StudioClassesView.as_view(), name='studio_classes_view'),
    path('<int:pk>/schedule/', StudioScheduleView.as_view(), name='studio_schedule_view'),
    path('<int:pk>/enrol/', EnrolView.as_view(), name='class_enrol_view'),
    path('<int:pk>/disenrol/', DisenrolView.as_view(), name='class_disenrol_view'),
    path('schedule/', UserClassScheduleView.as_view(), name='user_class_schedule_view'),
]