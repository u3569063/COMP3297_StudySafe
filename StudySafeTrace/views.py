from django.shortcuts import render

# Create your views here.
from datetime import timedelta
from django.views.generic import TemplateView
from api.models import *
import requests


class ViewContacts(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = self.get_contacts
        return context

    def get_contacts(self):
        endpoint = "http://localhost:8000/api/contacts/"
        get_response = requests.get(endpoint, json={"title": "get_close_contacts"})
        return get_response.json()