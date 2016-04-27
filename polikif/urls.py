from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),	
	url(r'^parti_accueil', views.parti_accueil, name='parti_accueil'),	
	url(r'^parti_presentation/(?P<id_parti>[0-9]+)', views.parti_presentation, name='parti_presentation'),	
	url(r'^programme_visualisation/(?P<id_parti>[0-9]+)', views.programme_visualisation, name='programme_visualisation'),	
	url(r'^membres_parti_visualisation/(?P<id_parti>[0-9]+)', views.membres_parti_visualisation, name='membres_parti_visualisation'),	
	url(r'^cellule_accueil', views.cellule_accueil, name='cellule_accueil'),
	url(r'^cellule_presentation/(?P<id_cellule>[0-9]+)', views.cellule_presentation, name='cellule_presentation'),
]