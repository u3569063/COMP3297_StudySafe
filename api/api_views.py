from datetime import timezone
from rest_framework import viewsets
from datetime import datetime, timedelta
from .models import *
from .serializers import *
from StudySafeCore.settings import DEBUG

ENTRY = "entry"
EXIT = "exit"

def visited_in_past_2_days(visit_date, test_date):
    return True if visit_date - test_date <= timedelta(days=2) else False

def stayed_for_more_than_30_mins(entry_time, exit_time):
    return True if exit_time - entry_time >= timedelta(minutes=30) else False

def list_close_contacts():
    close_contact_ids = list()
    for case in PositiveCase.objects.all():
        access_record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
        for visit in access_record:
            if (visit.Date_Time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
                for person in AccessRecord.objects.filter(Venue_Code=visit.Venue_Code):
                    if (person.Date_Time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
                        if not close_contact_ids.__contains__(person.HKU_ID):
                            close_contact_ids.append(person.HKU_ID)
    # close_contact_names = Member.objects.filter(HKU_ID__in=close_contact_ids).order_by("HKU_ID")
    close_contact_names = list()
    for person in Member.objects.all().order_by("HKU_ID"):
        if close_contact_ids.__contains__(person):
            close_contact_names.append(person)

    return close_contact_names

def list_disinfect_venues():
    # For each positive case, check whether they have visited any venues within 2 days
    disinfect_venue = list()
    positive_cases = PositiveCase.objects.all()
    for case in positive_cases:
        record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID).filter(Action=ENTRY)
        for visit in record:
            visit_date = visit.Date_Time.date()
            positive_date = case.Date_Of_Diagnosis
            if visited_in_past_2_days(visit_date, positive_date):
                # The Venue_Code of visit is suspicious
                # see if stayed for more than 30 mins
                entry_times = (
                    record.values('Date_Time')
                        .order_by('Date_Time')
                )
                exit_times = (
                    AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
                        .filter(Action=EXIT)
                        .values('Date_Time')
                        .order_by('Date_Time')
                )
               
                for i, en_t in enumerate(entry_times):
                    # if someone tested positive have not leave the venue
                    if i not in range(len(exit_times)):
                        timeDiff = datetime.now().astimezone()-en_t["Date_Time"]
                        if timeDiff >= timedelta(minutes=30):
                            disinfect_venue.append(visit.Venue_Code.pk)
                        # still need to check remaining records
                        continue
                    timeDiff = exit_times[i]["Date_Time"]-en_t["Date_Time"]
                    if timeDiff >= timedelta(minutes=30):
                        disinfect_venue.append(visit.Venue_Code.pk)

    disinfect_venue = Venue.objects.filter(Venue_Code__in=disinfect_venue).order_by("Venue_Code")
    return disinfect_venue

# Create your views here.
class DisinfectVenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = list_disinfect_venues()
    serializer_class = VenueSerializer

class CloseContactViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = list_close_contacts()
    serializer_class = MemberSerializer

class RecordViewSet(viewsets.ModelViewSet):
    queryset = AccessRecord.objects.all()
    serializer_class = AccessRecordSerializer