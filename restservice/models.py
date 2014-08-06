from django.db import models
from django.utils.translation import ugettext_lazy
from odk_logger.models.xform import XForm
from restservice import SERVICE_CHOICES


class RestService(models.Model):

    class Meta:
        app_label = 'restservice'
        unique_together = ('service_url', 'xform', 'name')

    service_url = models.URLField(ugettext_lazy("Service URL"))
    xform = models.ForeignKey(XForm)
    name = models.CharField(max_length=50, choices=SERVICE_CHOICES)

    def __unicode__(self):
        return u"%s:%s - %s" % (self.xform, self.long_name, self.service_url)

    def get_service_definition(self):
        m = __import__(''.join(['restservice.tasks']), globals(), \
                       locals(),[self.name])
        a = getattr(m,self.name) 
        return a

    @property
    def long_name(self):
        return [i for i in SERVICE_CHOICES if i[0]==self.name][0][1]



class RestServiceAnswer(models.Model):
    service = models.ForeignKey(RestService)
    instance = models.ForeignKey("odk_viewer.ParsedInstance")
    returnCode = models.CharField(max_length=4)
    returnText = models.TextField()
    iteration = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
