# Create your views here.
# a list of names and HKU IDs of those members identified as close contacts according
# to HKU’s definition (see Page 1). Sorted in increasing order of HKU ID.

from datetime import timedelta
from django.http import JsonResponse
from django.views.generic import TemplateView


from api.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def contacts(request, *args, **kwargs):
    data={}
    data["close_contact_names"] = get_contacts()
    return Response(data)

def get_contacts():
    close_contact_ids = list()
    for case in PositiveCases.objects.all():
        access_record = AccessRecord.objects.filter(hkuid=case.hkuid)
        for visit in access_record:
            if (visit.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
                for person in AccessRecord.objects.filter(venue_code=visit.venue_code):
                    if (person.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
                        if not close_contact_ids.__contains__(person.hkuid):
                            close_contact_ids.append(person.hkuid)
    close_contact_names = list()
    for person in Member.objects.all().order_by("hkuid"):
        if close_contact_ids.__contains__(person):
            close_contact_names.append(str(person.name))
    return close_contact_names

# class ViewContacts(TemplateView):
#     template_name = "contacts.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['contacts'] = self.get_contacts
#         return context
#
#     def get_contacts(self):
#         close_contact_ids = list()
#         for case in PositiveCases.objects.all():
#             access_record = AccessRecord.objects.filter(hkuid=case.hkuid)
#             for visit in access_record:
#                 if (visit.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
#                     for person in AccessRecord.objects.filter(venue_code=visit.venue_code):
#                         if (person.date_time.date() - case.date_of_diagnosis) <= timedelta(days=2):
#                             if not close_contact_ids.__contains__(person.hkuid):
#                                 close_contact_ids.append(person.hkuid)
#         close_contact_names = list()
#         for person in Member.objects.all().order_by("hkuid"):
#             if close_contact_ids.__contains__(person):
#                 close_contact_names.append(str(person.name))
#         return close_contact_names
