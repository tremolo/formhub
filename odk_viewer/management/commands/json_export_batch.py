from __future__ import print_function
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy
from odk_logger.models import XForm
from odk_viewer.models import Export
from utils.export_tools import generate_export

class Command(BaseCommand):
    help = ugettext_lazy('create a json export file. Usage="jason_export_batch user survey"')

    def handle(self, *args, **kwargs):
        c = 0
        print('Exporting json files for user={} survey={}'.format(args[0], args[1]))
        qs = XForm.objects.filter(user__username=args[0], id_string__contains=args[1])
        for form in qs:
            count = form.surveys.filter(is_deleted=False).count()
            if count:
                generate_export(Export.JSON_EXPORT, 'json', form.user.get_username(), form.id_string)
                c += 1
            else:
                print('No instances found for survey {}'.format(form.id_string))
        print("Created %d export(s)." % c)
