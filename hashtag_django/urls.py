'''
URL paths for the hashtag battle app 

@author:     PJ

'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import BattlesView, CreateBattleView
admin.autodiscover()

urlpatterns = patterns('',
    url("", include('django_socketio.urls')),
    url(r'^$', BattlesView.as_view(), name="main"),
    url(r'^create/$', CreateBattleView.as_view(), name="create"),
    url(r'^admin/', include(admin.site.urls)),
    
)
