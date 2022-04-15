# Create your views here.
# a list of names and HKU IDs of those members identified as close contacts according
# to HKU’s definition (see Page 1). Sorted in increasing order of HKU ID.

from datetime import timedelta
from rest_framework import viewsets
from api.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
#
# @api_view(['GET'])
# def contacts(request, *args, **kwargs):
#     data={}
#     data["close_contact_names"] = get_contacts()
#     return Response(data)

def get_contacts():
    close_contact_ids = list()
    for case in PositiveCase.objects.all():
        access_record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
        for visit in access_record:
            if (visit.Date_Time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
                for person in AccessRecord.objects.filter(Venue_Code=visit.Venue_Code):
                    if (person.Date_Time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
                        if not close_contact_ids.__contains__(person.HKU_ID):
                            close_contact_ids.append(person.HKU_ID)
    close_contact_names = list()
    for person in Member.objects.all().order_by("HKU_ID"):
        if close_contact_ids.__contains__(person):
            close_contact_names.append(person)
    return close_contact_names

class CloseContactListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_contacts()
    serializer_class = MemberSerializer


