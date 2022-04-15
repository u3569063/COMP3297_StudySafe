from datetime import timedelta
from django.test import TestCase


# Create your tests here.
# query
# List all
from api.models import *
from datetime import timedelta

class ListAsQuerySet(list):

    def __init__(self, *args, model, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)

    def filter(self, *args, **kwargs):
        return self  # filter ignoring, but you can impl custom filter

    def order_by(self, *args, **kwargs):
        return self
