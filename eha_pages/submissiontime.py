"""
submissiontime.py --> Defines Submission-time Validation callback routines for eHealthAfrica.

These routines are called from validations.py when a user "submits" an X-form to the formhub site

callbacks must be a Python callable (i.e. function) which is used to validate one row of data from a form.
- - - - - -
said function will be called with an argument list like the following:
def dummy_callable(form_name, xml_root, request, username, uuid, media_files):
    for element in xml_root:
        pass  # each field in the X-form will appear here

--> return None to continue normal processing,
 or return an utils.logger_tools.OpenRosaResponseNotAcceptable Exception to inhibit record loading with a message
"""
from utils.logger_tools import OpenRosaResponseNotAcceptable

# def testing_callback(form_name, xml_root, request, username, uuid, media_files):
#     """ callback function used for automatic django testing """
#     if any([element.tag == 'reject_this' and element.text == "1" for element in xml_root]):
#         return OpenRosaResponseNotAcceptable('Record refused because "reject_this" was True.')

# # # # ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
##  The following ugly code is hard wired for the HHsurvey project.
## It should be removed from the eHa formhub source as soon after the project
## is complete as possible.
##   Be very careful about using this as a model for future submission-time validations.
##
from django.db.models.expressions import F
from eha_pages.models import RealTime_Count
## define the names of the HHsurvey LGAs from their code enum values
LGA_NAMES = {'1': 'Albasu', '2': 'Gurun Mallam', '3': 'Danbatta'}

def HH_callback(form_name, xml_root, request, username, uuid, media_files):
    """ callback function used for HHsurvey processing """
    ## the only element we care about for counting is the LGA
    lgas = xml_root.find('lga')
    ## convert the LGA code number to its name
    lga = LGA_NAMES[lgas.text]
    ## try to get our count record (should usually succeed)
    try:
        # increment the count in a single operation to eliminate race conditions
        RealTime_Count.objects.filter(survey__id_string=form_name, group=lga).update(count=F('count')+1)
    except RealTime_Count.DoesNotExist:
        rtc = RealTime_Count(survey=form_name, group=lga, group_name='LGA', count=1)
        rtc.save()
    ##rtc = RealTime_Count.objects.get(survey__id_string=form_name, group=lga)
    ##if lga == 'Danbatta': return OpenRosaResponseNotAcceptable('### temporary testing kludge') ### -- remove this !!!
# # # # ! ! ! ! ! ! end of ugly code (remove this) ! ! ! ! ! ! ! ! ! ! ! ! ! !
