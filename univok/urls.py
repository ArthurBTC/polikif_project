from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
	url(r'^evenement/(?P<id_event>[0-9]+)', views.eventViewer, name='eventViewer'),
	url(r'^idees/(?P<id_event>[0-9]+)', views.ideasViewer, name='ideasViewer'),
	url(r'^sentences', views.sentencesConverter, name='sentencesConverter'),
]