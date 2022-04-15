from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *
from .views import CloseContactListViewSet
router = DefaultRouter()
router.register(r'venues', DisinfectVenueViewSet, 'venues')
router.register(r'contacts', CloseContactListViewSet,'contacts')

urlpatterns = [
    path('', include(router.urls)),
]
