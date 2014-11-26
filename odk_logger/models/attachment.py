import os
import mimetypes

from tempfile import NamedTemporaryFile
from hashlib import md5
from django.core.files.storage import get_storage_class
from django.db import models

from instance import Instance


def upload_to(instance, filename):
    return os.path.join(
        instance.instance.user.username,
        'attachments',
        os.path.split(filename)[1])


class Attachment(models.Model):
    instance = models.ForeignKey(Instance, related_name="attachments")
    media_file = models.FileField(upload_to=upload_to)
    
    # This is because the media_file might rename the filename (if it exists)
    # But we still save the json into MongoDB so the objects.get will not work
    # That is why we save the original file name too, just so we don't loose it
    # and we can retrieve it, if we need to. 
    original_name = models.CharField(max_length=250, null=True, blank=True)

    mimetype = models.CharField(
        max_length=50, null=False, blank=True, default='')

    class Meta:
        app_label = 'odk_logger'

    def save(self, *args, **kwargs):
        if self.media_file and self.mimetype == '':
            # guess mimetype
            mimetype, encoding = mimetypes.guess_type(self.media_file.name)
            if mimetype:
                self.mimetype = mimetype
        
        if not self.original_name:
            self.original_name = self.media_file.name
        
        super(Attachment, self).save(*args, **kwargs)

    @property
    def full_filepath(self):
        if self.media_file:
            default_storage = get_storage_class()()
            try:
                return default_storage.path(self.media_file.name)
            except NotImplementedError:
                # read file from s3
                name, ext = os.path.splitext(self.media_file.name)
                tmp = NamedTemporaryFile(suffix=ext, delete=False)
                f = default_storage.open(self.media_file.name)
                tmp.write(f.read())
                tmp.close()
                return tmp.name
        return None

    @property
    def file_hash(self):
        if self.media_file.storage.exists(self.media_file.name):
            return u'%s' % md5(self.media_file.read()).hexdigest()
        return u''

    @property
    def filename(self):
        return os.path.basename(self.media_file.name)
