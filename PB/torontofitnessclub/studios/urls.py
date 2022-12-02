from django.urls import path
from .views import StudioListView, StudioDetailView

urlpatterns = [
    path('', StudioListView.as_view(), name='studio_list'),
    path('<int:pk>/', StudioDetailView.as_view(), name='studio_detail'),
]