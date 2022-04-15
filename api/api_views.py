from rest_framework import viewsets
from datetime import timedelta
from .models import *
from .serializers import *

def list_disinfect_venues():
    # For each positive case, check whether they have visited any venues within 2 days
    disinfect_venue = list()
    close_contacts = list()

    positive_cases = PositiveCase.objects.all()

    def visited_in_past_2_days(visit_date, test_date):
        return True if visit_date - test_date <= timedelta(days=2) else False

    def stayed_for_more_than_30_mins(entry_time, exit_time):
        return True if exit_time - entry_time >= timedelta(minutes=30) else False


    ENTRY = "entry"
    EXIT = "exit"

    positive_cases = PositiveCase.objects.all()
    for case in positive_cases:
        record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
        for visit in record:
            visit_date = visit.Date_Time.date()
            positive_date = case.Date_Of_Diagnosis
            if visited_in_past_2_days(visit_date, positive_date):
                # The Venue_Code of visit is suspicious
                # see if stayed for more than 30 mins
                entry_times = (
                    record.filter(HKU_ID=case.HKU_ID)
                        .filter(Action=ENTRY)
                        .values('Date_Time')
                        .order_by('Date_Time')
                )
                exit_times = (
                    record.filter(HKU_ID=case.HKU_ID)
                        .filter(Action=EXIT)
                        .values('Date_Time')
                        .order_by('Date_Time')
                )
                for i, e_t in enumerate(entry_times):
                    if i not in range(len(exit_times)):
                        # add venue to disinfect list
                        disinfect_venue.append(visit.Venue_Code.pk)
                        continue
                    if stayed_for_more_than_30_mins(exit_times[i], e_t):
                        disinfect_venue.append(visit.Venue_Code.pk)

    disinfect_venue = Venue.objects.filter(Venue_Code__in=disinfect_venue).order_by("Venue_Code")
    return disinfect_venue

# Create your views here.
class DisinfectVenueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = list_disinfect_venues()
    serializer_class = VenueSerializer