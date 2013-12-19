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
# def testing_callback(form_name, xml_root, request, username, uuid, media_files):
#     """ callback function used for automatic django testing """
#     if any([element.tag == 'reject_this' and element.text == "1" for element in xml_root]):
#         return OpenRosaResponseNotAcceptable('Record refused because "reject_this" was True.')

class HH_global_kludge(object):
    """ quick and dirty data structure to hold counts for the HHsurvey  project.
    Delete this ugly monster when the project is complete!
    Counters are kept a class variable and are altered at run time.  Yeech!
    """
    counters = {}

from eha_pages.models import RealTime_Count
def HH_callback(form_name, xml_root, request, username, uuid, media_files):
    """ callback function used for automatic django testing """
    if any([element.tag == 'reject_this' and element.text == "1" for element in xml_root]):
        return OpenRosaResponseNotAcceptable('Record refused because "reject_this" was True.')
