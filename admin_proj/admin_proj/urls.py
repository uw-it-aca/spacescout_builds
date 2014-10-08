from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'spacescout.views.home', name='home'),
    # url(r'^spacescout/', include('spotseeker.foo.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'spacescout_admin/registration/login.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^djangoadmin/', include(admin.site.urls)),

    url(r'^', include('spacescout_admin.urls')),
)

urlpatterns += staticfiles_urlpatterns()
