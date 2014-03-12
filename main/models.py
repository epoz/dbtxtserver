from django.db import models
from django.contrib.auth.models import User
import textbase

class Collection(models.Model):
    name = models.CharField(max_length=250)
    # Field to use for ID
    # FIeld to use for display template selection
    def __unicode__(self):
        return self.name

class Record(models.Model):
    uid = models.CharField(max_length=32, primary_key=True)
    prev = models.ForeignKey('self', null=True, blank=True)
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection, related_name='records')
    timestamp = models.DateTimeField(auto_now_add=True)    
    data = models.TextField()

    def obj(self):
        tmp = textbase.TextBase(self.data.encode('utf8'))
        if len(tmp) > 0:
            return tmp[0]
        return {}

class Template(models.Model):
    name = models.CharField(max_length=32, primary_key=True)
    content = models.TextField()