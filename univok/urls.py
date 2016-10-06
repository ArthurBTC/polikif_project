from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
	url(r'^evenement/(?P<id_event>[0-9]+)', views.eventViewer, name='eventViewer'),
	url(r'^idees/(?P<id_event>[0-9]+)', views.ideasViewer, name='ideasViewer'),
	url(r'^sentences/(?P<id_event>[0-9]+)', views.sentencesConverter, name='sentencesConverter'),
	url(r'^collectif', views.collectif, name='collectif'),
    url(r'^ajax_newquestion', views.ajax_newquestion, name='ajax_newquestion'),
    url(r'^finalBuilder', views.finalBuilder, name='finalBuilder'),
]