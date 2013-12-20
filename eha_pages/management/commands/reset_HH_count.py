"""
Restore HHsurvey  counter to agree with actual number of submissions in the database
"""
from __future__ import print_function

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy
from odk_logger.models import Instance, XForm
from eha_pages.models import RealTime_Count
from odk_logger.xform_instance_parser import clean_and_parse_xml

HH_FORM_ID = 'build_HHsurvey'
LGA_NAMES = {'1': 'Albasu', '2': 'Gurun Mallam', '3': 'Danbatta'}

class Command(BaseCommand):
    help = ugettext_lazy('Reset submission count to actual instances in xml')

    def handle(self, *args, **kwargs):
        count = {}
        myxforms = XForm.objects.filter(id_string__startswith=HH_FORM_ID)
        if len(myxforms) != 1:
            CommandError('Failed to find single instance of {} survey'.format(HH_FORM_ID))
        myxform = myxforms[0]
        for form in Instance.objects.filter(xform=myxform):
            xm = clean_and_parse_xml(form.xml)
            lgas = xm.getElementsByTagName('lga')
            lga = LGA_NAMES[lgas[0].childNodes[0].data]
            try:
                count[lga] += 1
            except KeyError:
                count[lga] = 1

        for key in count:
            try:
                rtc = RealTime_Count.objects.get(group=key)
            except RealTime_Count.DoesNotExist:
                rtc = RealTime_Count()
                rtc.survey = myxform
                rtc.group = key
                rtc.group_name = 'LGA'
            rtc.count = count[key]
            print('LGA {}={}'.format(key, rtc.count))
            rtc.save()
