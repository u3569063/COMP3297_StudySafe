from datetime import datetime, timedelta

from rest_framework import viewsets

from .serializers import *

ENTRY = "entry"
EXIT = "exit"

def visited_in_past_2_days(visit_date, test_date):
    return True if visit_date - test_date <= timedelta(days=2) else False


def stayed_for_more_than_30_mins(entry_time, exit_time):
    return True if exit_time - entry_time >= timedelta(minutes=30) else False


def append_cc_ids_for_record(venue_code: Venue.Venue_Code, case_en_t: AccessRecord.Date_Time,
                             case_ex_t: AccessRecord.Date_Time, close_contact_ids):
    # if suspicious record did not stay for more than 30 mins, directly return
    if not stayed_for_more_than_30_mins(case_en_t, case_ex_t):
        return close_contact_ids

    for record in AccessRecord.objects \
            .filter(Venue_Code=venue_code) \
            .filter(Action=ENTRY) \
            .order_by('Date_Time'):
        close_contact_ids.append(record.HKU_ID)
        if close_contact_ids.__contains__(record.HKU_ID):
            continue

        entry_times = (
            record.values('Date_Time')
                .order_by('Date_Time')
        )

        exit_times = (
            AccessRecord.objects
                .filter(HKU_ID=record.HKU_ID)
                .filter(Venue_Code=venue_code)
                .filter(Action=EXIT)
                .values('Date_Time')
                .order_by('Date_Time')
        )

        for i, record_ent_t in enumerate(entry_times):
            # check if record contact with case for more than 30 mins
            if record_ent_t.date() == case_en_t.date():
                # still in venue
                if i not in range(len(exit_times)):
                    time_diff1 = datetime.now().astimezone() - record_ent_t["Date_Time"]
                    time_diff2 = datetime.now().astimezone() - case_en_t
                else:
                    time_diff1 = exit_times[i]["Date_Time"] - record_ent_t["Date_Time"]
                    time_diff2 = exit_times[i]["Date_Time"] - case_en_t
                time_diff3 = case_ex_t - record_ent_t["Date_Time"]
                if time_diff1 >= timedelta(minutes=30) \
                        and time_diff2 >= timedelta(minutes=30) \
                        and time_diff3 >= timedelta(minutes=30):
                    close_contact_ids.append(record.HKU_ID)
                    break


def list_close_contacts_ids():
    close_contact_ids = list()
    positive_cases = PositiveCase.objects.all()
    for case in positive_cases:
        records = AccessRecord.objects.filter(HKU_ID=case.HKU_ID).filter(Action=ENTRY)
        for visit in records:
            visit_date = visit.Date_Time.date()
            positive_date = case.Date_Of_Diagnosis
            if visited_in_past_2_days(visit_date, positive_date):
                # see if stayed for > 30 mins
                entry_times = (
                    records.values('Date_Time')
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
                        append_cc_ids_for_record(visit.Venue_Code, en_t["Date_Time"],
                                                 datetime.now().astimezone(), close_contact_ids)
                    else:
                        append_cc_ids_for_record(visit.Venue_Code, en_t["Date_Time"],
                                                 exit_times[i]["Date_Time"], close_contact_ids)
    return close_contact_ids


def list_close_contacts():
    close_contact_ids = list_close_contacts_ids()
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
        record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID).filter(Action=ENTRY).order_by('Date_Time')
        for i in range(len(record)):
            visit = record[i]
            visit_date = visit.Date_Time.date()
            positive_date = case.Date_Of_Diagnosis
            if visited_in_past_2_days(visit_date, positive_date):
                # The Venue_Code of visit is suspicious
                # see if stayed for more than 30 mins
                record_e = (
                    AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
                        .filter(Action=EXIT)
                        .order_by('Date_Time')
                )
                entry_t, exit_t = visit.Date_Time, 0
                if i not in range(len(record_e)):
                    exit_t = datetime.now().astimezone()
                else:
                    exit_t = record_e[i].Date_Time
                if stayed_for_more_than_30_mins(entry_t, exit_t):
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

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer

