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
    url(r'^deepview/(?P<id_event>[0-9]+)', views.deepview, name='deepview'),
    url(r'^simpleGraphViewer/(?P<id_show>[0-9]+)', views.simpleGraphViewer, name='simpleGraphViewer'),
    
    url(r'^reviewAsList/(?P<id_event>[0-9]+)', views.reviewAsList, name='reviewAsList'),
    url(r'^reviewAsListBuilder/(?P<id_event>[0-9]+)', views.reviewAsListBuilder, name='reviewAsListBuilder'),
    
    url(r'^propsAuthorGenerator', views.propsAuthorGenerator, name='propsAuthorGenerator'),
    url(r'^anim/(?P<id_event>[0-9]+)', views.animViewer, name='animViewer'),
    
    url(r'^duplicateShow/(?P<id_show>[0-9]+)', views.duplicateShow, name='duplicateShow'),
    url(r'^reviewSimple/(?P<id_show>[0-9]+)', views.reviewSimple, name='reviewSimple'),
    
]