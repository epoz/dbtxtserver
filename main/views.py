from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse

import textbase
import models
import uuid

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
    return render(request, 'upload.html', context)

def record_edit(request, pk):
    record = models.Record.objects.get(pk=pk)
    context = {'record': record}
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

class RecordListView(ListView):
    paginate_by = 20
    model = models.Record

    def get_context_data(self, **kwargs):
        context = super(RecordListView, self).get_context_data(**kwargs)
        context['collection'] = self.collection
        return context

    def get_queryset(self):
        self.collection = get_object_or_404(models.Collection, id=self.kwargs['collection'])
        return models.Record.objects.filter(collection = self.collection)

class CollectionListView(ListView):
    model = models.Collection

class RecordDetailView(DetailView):

    queryset = models.Record.objects.all()

    # def get_object(self):
    #     object = super(RecordDetailView, self).get_object()
    #     # Return the object
    #     return object