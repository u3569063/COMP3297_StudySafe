from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *

router = DefaultRouter()
router.register(r'disinfectvenues', DisinfectVenueViewSet, 'disinfectvenues')
router.register(r'closecontacts', CloseContactViewSet,'closecontacts')
router.register(r'records', RecordViewSet, 'records')
router.register(r'venues',  VenueViewSet, 'venues')
router.register(r'members', MemberViewSet, 'members')

urlpatterns = [
    path('', include(router.urls)),
]
urlpatterns += router.urls
