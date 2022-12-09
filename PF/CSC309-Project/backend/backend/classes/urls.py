from django.urls import path

from . import views

app_name = 'classes'
urlpatterns = [
    path('search/', views.class_search_view),
    # path('add/', views.studio_create_view),
    # path('<int:pk>/add/', ClassCreateApiView.as_view())
]