<<<<<<< HEAD
from django.urls import path

from api import views

urlpatterns = [
    # path('contacts/',
    #      views.ViewContacts.as_view(),
    #      name='contatcts-api'
    #      ),
    path('contacts/', views.contacts),
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import *
from .views import CloseContactListViewSet
router = DefaultRouter()
router.register(r'venues', DisinfectVenueViewSet, 'venues')
router.register(r'contacts', CloseContactListViewSet,'contacts')

urlpatterns = [
    path('', include(router.urls)),
>>>>>>> 0f523fa... SS-22 contact add to framework
]
