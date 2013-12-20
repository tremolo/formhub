from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from odk_logger.models.xform import XForm

class UserSeesThis(models.Model):
    user = models.ForeignKey(User, related_name='sees_this')
    form = models.ForeignKey(XForm, related_name='seen_by')
    class Meta:
        verbose_name_plural = "UserSeesThese"
        ordering = (['user', 'form'])
    def __unicode__(self):
        return '{} sees {}'.format(self.user, self.form.id_string)

class RealTime_Count(models.Model):
    survey = models.ForeignKey(XForm, related_name='counter')
    group = models.CharField('group', max_length=100, blank=True, null=True)
    group_name = models.CharField('grouping', max_length=30)
    count = models.IntegerField('count')
    class Meta:
        ordering = (['survey', 'group'])
    def __unicode__(self):
        return '{} {} {} {}'.format(self.group_name, self.group, self.count, self.survey)

