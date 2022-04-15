from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'venues', DisinfectVenueViewSet, 'venues')
router.register(r'records', RecordViewSet, 'records')
router.register(r'contacts', CloseContactViewSet,'contacts')

urlpatterns = [
    path('', include(router.urls)),
]
