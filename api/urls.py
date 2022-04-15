from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'venues', DisinfectVenueViewSet, 'venues')

urlpatterns = [
    path('', include(router.urls)),
    path('contacts/', views.contacts),
]
