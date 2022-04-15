from django.urls import path
from api import api_views

urlpatterns = [
    path('contacts/',
         api_views.ViewContacts.as_view(),
         name='contatcts-api'
         ),
]
