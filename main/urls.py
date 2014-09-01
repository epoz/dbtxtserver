from django.conf.urls import patterns, url
from views import CollectionListView, RecordListView, RecordEditsListView, RecordDetailView

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),
    url(r'^help/(?P<page>[0-9a-zA-Z]*)$', 'main.views.help', name='help'),
    url(r'^login$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout$', 'main.views.logout_view', name='logout'),
    url(r'^upload/$', 'main.views.upload', name='upload'),
    url(r'^collections/$', CollectionListView.as_view(), name='collection-list'),
    url(r'^collections/(?P<collection>[0-9+])/edits$', RecordEditsListView.as_view(), name='collection-edits'),
    url(r'^collections/(?P<collection>[0-9+])/$', RecordListView.as_view(), name='record-list'),
    url(r'^records/(?P<pk>[0-9a-f]+)/$', RecordDetailView.as_view(), name='record-detail'),
    url(r'^records/(?P<pk>[0-9a-f]+)/edit$', 'main.views.record_edit', name='record-edit'),
    url(r'^records/(?P<pk>[0-9a-f]+)/save$', 'main.views.record_save', name='record-save'),
    url(r'^search$', 'main.views.search', name='searchall'),
)
