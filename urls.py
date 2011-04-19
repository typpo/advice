import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^notes/', include('notes.urls')),

    (r'^notes/login/', 'django.contrib.auth.views.login'),
    (r'^notes/logout/', 'django.contrib.auth.views.logout'),
    (r'^notes/password_change/', 'django.contrib.auth.views.password_change'),
    (r'^notes/password_change_done/', 'django.contrib.auth.views.password_change'),

    # TODO config web server to do this
    (r'^notes/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^notes/admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^notes/admin/', include(admin.site.urls)),
)
