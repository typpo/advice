from django.conf.urls.defaults import *

urlpatterns = patterns('notes.views',
    (r'^$', 'index'),
    (r'^c/$', 'company_index'),
    (r'^p/$', 'position_index'),
    (r'^c/(?P<company_id>\d+)/$', 'company'),
    (r'^c/(?P<company_name>.+)/$', 'company_by_name'),
    (r'^p/(?P<position_id>\d+)/$', 'position'),
    (r'^p/(?P<position_title>.+)/$', 'position_by_title'),
    (r'^i/$', 'interviews'),
    (r'^edit/(?P<id>\d+)/$', 'edit_interview'),
    (r'^editquestion/(?P<id>\d+)/$', 'edit_question'),
    (r'^companytags/$', 'companytags'),
    (r'^positiontags/$', 'positiontags'),
    (r'^add/$', 'add'),

    (r'^signup/$', 'signup'),

    ##### 

)
