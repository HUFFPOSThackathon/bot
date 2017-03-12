from django.conf.urls import patterns, include, url
from django.contrib import admin
import bot.views as v 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'huffpost.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook_auth/?$' , v.MyChatBotView.as_view())
)
