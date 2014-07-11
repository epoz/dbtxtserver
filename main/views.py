from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.conf import settings

import textbase
import models
import uuid

def help(request, page):
    if not page:
        page = "index"
    return render(request, 'help/%s.html' % page)

def home(request):
    context = {'collections':models.Collection.objects.all()}
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('/')

def upload(request):
    context = {'collections':models.Collection.objects.all()}
    if request.method == 'POST' and 'dbtxtfile' in request.FILES:
        collection = models.Collection.objects.get(id=request.POST.get('collection'))
        dbtxtfile = textbase.TextBase(request.FILES['dbtxtfile'])
        for d in dbtxtfile:
            models.Record.objects.create(collection=collection, uid=uuid.uuid4().hex,
                                         user=request.user, data=textbase.dumpdict(d))
        context['size'] = len(dbtxtfile)
        collection.index()

    return render(request, 'upload.html', context)

def record_edit(request, pk):
    record = models.Record.objects.get(pk=pk)
    context = {'record': record, 'collection': record.collection}
    return render(request, 'main/record_edit.html', context)

@require_POST
def record_save(request, pk):
    record = models.Record.objects.get(pk=pk)
    data = request.POST.get('data')
    if data != record.data:
        new_record = models.Record.objects.create(collection=record.collection, uid=uuid.uuid4().hex,
                                         user=request.user, data=data)
        record.newer = new_record
        record.save()        
    return HttpResponse(reverse('record-detail', kwargs={'pk':new_record.pk}), content_type='text/plain')

def search(request):
    q = request.GET.get('q')
    return render(request, 'index.html', {'q':q})

class RecordListView(ListView):
    paginate_by = 50
    model = models.Record

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        context['collection'] = self.collection
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        self.collection = get_object_or_404(models.Collection, id=self.kwargs['collection'])
        q = self.request.GET.get('q')
        if not q:
            return self.collection.records.all()
        return self.collection.search_queryset(q)

class CollectionListView(ListView):
    model = models.Collection

class RecordDetailView(DetailView):

    queryset = models.Record.objects.all()

    def get_context_data(self, **kwargs):
        context = super(RecordDetailView, self).get_context_data(**kwargs)
        record = super(RecordDetailView, self).get_object()
        context['collection'] = record.collection
        return context

    # def get_object(self):
    #     object = super(RecordDetailView, self).get_object()
    #     # Return the object
    #     return object