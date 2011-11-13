from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'reaju_bomb.root.views.index'),
    (r'^oauth$', 'reaju_bomb.root.views.oauth'),
    (r'^signin$', 'reaju_bomb.root.views.signin'),
    (r'^signout$', 'reaju_bomb.root.views.signout'),
    (r'^post$', 'reaju_bomb.root.views.post'),
)
