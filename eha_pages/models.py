from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from odk_logger.models.xform import XForm

class UserSeesThis(models.Model):
    user = models.ForeignKey(User, related_name='sees_this')
    form = models.ForeignKey(XForm, related_name='seen_by')
    class Meta:
        verbose_name_plural = "UserSeesThese"
    def __unicode__(self):
        return '{} sees {}'.format(User.get_short_name(), XForm.id_string)

class RealTime_Count(models.Model):
    survey = models.ForeignKey(XForm, related_name='counter')
    group = models.CharField('group', max_length=100, blank=True, null=True)
    group_name = models.CharField('grouping', max_length=30)
    count = models.IntegerField('count')
    def __unicode__(self):
        return '{} {} {} {}'.format(group_name, group, count, survey)

