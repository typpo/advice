from django.conf.urls.defaults import *

urlpatterns = patterns('notes.views',
    (r'^$', 'company_index'),
    (r'^positions/$', 'position_index'),
    (r'^c/(?P<company_id>\d+)/$', 'company'),
    (r'^c/(?P<company_name>.+)/$', 'company_by_name'),
    (r'^c/(?P<company_name>.+)/$', 'company_by_name'),
    (r'^i/$', 'interviews'),
)
