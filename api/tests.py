from datetime import timedelta
from django.test import TestCase

# Create your tests here.
# query
# List all
from api.models import *
from datetime import timedelta

# For each positive case, check whether they have visited any venues within 2 days
venues_to_be_cleaned = list()
close_contacts = list()
for case in PositiveCases.objects.all():
    access_record = AccessRecord.objects.filter(hkuid=case.hkuid)
    for visit in access_record:
        if (visit.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
            # this venue needs to be cleaned
            venues_to_be_cleaned.append(visit.venue_code)
            # get close contacts, they are those who share the same venue_code
            for person in AccessRecord.objects.filter(venue_code=visit.venue_code):
                if (person.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
                    close_contacts.append(person.hkuid)


print(venues_to_be_cleaned)
print(close_contacts)

# close contacts