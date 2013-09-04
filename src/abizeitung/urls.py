from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r"^login$", "abizeitung.views.session.login"),
    url(r"^logout", "abizeitung.views.session.logout"),
    
    url(r"^$", RedirectView.as_view(url="/student")),
    url(r"^student$", "abizeitung.views.student.edit")
    
    # Examples:
    # url(r'^$', 'abizeitung.views.home', name='home'),
    # url(r'^abizeitung/', include('abizeitung.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
