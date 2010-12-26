import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^notes/', include('notes.urls')),
    (r'^login/', 'django.contrib.auth.views.login'),
    (r'^logout/', 'django.contrib.auth.views.logout'),
    (r'^password_change/', 'django.contrib.auth.views.password_change'),
    (r'^password_change_done/', 'django.contrib.auth.views.password_change'),

    # TODO config web server to do this
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^tinymce/', include('tinymce.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
