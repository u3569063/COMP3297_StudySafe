from django.shortcuts import render

# Create your views here.

from datetime import timedelta

from django.views.generic import TemplateView

from api.models import *


class ViewContacts(TemplateView):
    template_name = "contacts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = self.get_contacts
        return context

    def get_contacts(self):
        # close_contact_ids = list()
        # for case in PositiveCase.objects.all():
        #     access_record = AccessRecord.objects.filter(HKU_ID=case.HKU_ID)
        #     for visit in access_record:
        #         if (visit.Date_Time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
        #             for person in AccessRecord.objects.filter(Venue_Code=visit.Venue_Code):
        #                 if (person.date_time.date() - case.Date_Of_Diagnosis) <= timedelta(days=2):
        #                     if not close_contact_ids.__contains__(person.hkuid):
        #                         close_contact_ids.append(person.hkuid)
        # close_contact_names = list()
        # for person in Member.objects.all().order_by("hkuid"):
        #     if close_contact_ids.__contains__(person):
        #         close_contact_names.append(str(person.name))
        # return close_contact_names
        return