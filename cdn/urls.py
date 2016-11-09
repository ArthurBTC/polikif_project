from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
	url(r'^getEvent/(?P<idEvent>[0-9]+)', views.getEvent, name='getEvent'),	
	url(r'^getAllEvents', views.getAllEvents, name='getAllEvents'),	
	url(r'^updateMembers', views.updateMembers, name='updateMembers'),
	url(r'^updatePastEvents', views.updatePastEvents, name='updatePastEvents'),
	url(r'^updatePresence/(?P<idEvent>[0-9]+)', views.updatePresence, name='updatePresence'),
	url(r'^updatePresences', views.updatePresences, name='updatePresences'),
	url(r'^memberView/(?P<idmember>[0-9]+)', views.memberView, name='memberView'),	
	
	url(r'^organisation', views.organisation, name='organisation'),
    url(r'^cafeines', views.cafeines, name='cafeines'),
    url(r'^question', views.question, name='question'),
]