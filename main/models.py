from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.template.defaultfilters import slugify
import textbase
import elasticsearch, elasticsearch.helpers

class Collection(models.Model):
    name = models.CharField(max_length=250)
    # Field to use for ID
    # FIeld to use for display template selection
    
    def __unicode__(self):
        return self.name
    
    def index_iterator(self):
        for record in self.records.all():
            o = record.obj()
            o['_index'] =  settings.ES_INDEX_NAME + '_' + slugify(self.name)
            o['_type'] = 'obj'
            o['_id'] = record.uid
            yield o
    
    def index(self):
        success_count, errors = elasticsearch.helpers.bulk(elasticsearch.Elasticsearch(), 
                                                           self.index_iterator(),
                                                           chunk_size=9999)
        return success_count, errors

    def search_queryset(self, q):
        es = elasticsearch.Elasticsearch()
        results = es.search(index=settings.ES_INDEX_NAME + '_' + slugify(self.name),
                            q=q, size=999, default_operator='AND')

        ids = [x['_id'] for x in results['hits']['hits']]
        return self.records.filter(pk__in=ids)


class Record(models.Model):
    uid = models.CharField(max_length=32, primary_key=True)
    newer = models.ForeignKey('self', null=True, blank=True, related_name='older')
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