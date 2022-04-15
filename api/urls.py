from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'venues', DisinfectVenueViewSet, 'venues')
# router.register(r'contacts', CloseContactViewSet, 'contacts')
router.register(r'records', RecordViewSet, 'records')

urlpatterns = [
    path('', include(router.urls)),
]
