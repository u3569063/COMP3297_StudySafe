from django.urls import path

from api import views

urlpatterns = [
    path('contacts/',
         views.ViewContacts.as_view(),
         name='contatcts-api'
         ),
]
