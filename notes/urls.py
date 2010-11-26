from django.conf.urls.defaults import *

urlpatterns = patterns('notes.views',
    (r'^$', 'index'),
    (r'^c/$', 'company_index'),
    (r'^p/$', 'position_index'),
    (r'^c/(?P<company_id>\d+)/$', 'company'),
    (r'^c/(?P<company_name>.+)/$', 'company_by_name'),
    (r'^i/$', 'interviews'),
)
