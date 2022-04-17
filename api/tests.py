from argparse import Action
from asyncio.windows_events import NULL
from datetime import datetime, timedelta
from django.test import TestCase


# Create your tests here.
# query
# List all
from api.models import *
from datetime import timedelta
ENTRY = "entry"
EXIT = "exit"


def visited_in_past_2_days(visit_date, test_date):
    return True if test_date - visit_date <= timedelta(days=2) else False

def stayed_for_more_than_30_mins(entry_time, exit_time):
    return True if exit_time - entry_time >= timedelta(minutes=30) else False

def list_disinfect_venues():
    # For each positive case, check whether they have visited any venues within 2 days
    disinfect_venue = list()
    positive_cases = PositiveCase.objects.all()
    for case in positive_cases:
        record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID).filter(Action=ENTRY).order_by('Date_Time')
        for i in range(len(record)):
            visit = record[i]
            visit_date = visit.Date_Time.date()
            positive_date = case.Date_Of_Diagnosis
            if visited_in_past_2_days(visit_date, positive_date):
                disinfect_venue.append(visit.Venue_Code.Venue_Code)

    disinfect_venue = Venue.objects.filter(Venue_Code__in=disinfect_venue).order_by("Venue_Code")
    return disinfect_venue

def list_members():
    members = Member.objects.all()
    for member in members: 
        print(member.HKU_ID)

#print(list_members())
print(list_disinfect_venues())