"""EmailDelivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .import views

urlpatterns = [
    url(r'^drafts$',                                views.drafts,               name = 'drafts'),
    url(r'^sentMail$',                              views.sentMail,             name = 'sentMail'),
    url(r'^profile$',                               views.profile,              name = 'profile'),
    url(r'^sendMail$',                              views.sendMail,             name = 'sendMail'),
    url(r'^saveDraft$',                             views.saveDraft,            name = 'saveDraft'),
    url(r'^downloadImage$',                         views.downloadImage,        name = 'downloadImage'),
    url(r'^(?P<messageID>\d+)/forward$',            views.forward,              name = 'forward'),
    url(r'^(?P<draftID>\d+)/viewDraft$',            views.viewDraft,            name = 'viewDraft'),
    url(r'^(?P<targetUserID>\d+)/reply$',           views.reply,                name = 'reply'),
    url(r'^(?P<messageID>\d+)/viewMessage$',        views.viewMessage,          name = 'viewMessage'),
    url(r'^(?P<messageID>\d+)/viewOutboxMessage$',  views.viewOutboxMessage,    name = 'viewOutboxMessage'),
    url(r'^inbox/(?P<messageID>\d+)/delete$',       views.deleteFromInbox,      name = 'deleteFromInbox'),

    url(r'^(?P<messageID>\d+)/viewInboxMessage$',        views.viewInboxMessage,          name = 'viewInboxMessage'),
    url(r'^getMessage/(?P<messageID>\d+)$',        views.getMessage,          name = 'getMessage'),
]
