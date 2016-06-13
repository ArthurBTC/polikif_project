from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),	
	
	url(r'^accueilPartis', views.accueilPartis, name='accueilPartis'),	
	
	url(r'^partiPresentation/(?P<id_parti>[0-9]+)', views.partiPresentation, name='partiPresentation'),	
	url(r'^partiProgramme/(?P<id_parti>[0-9]+)', views.partiProgramme, name='partiProgramme'),	
	url(r'^partiMembres/(?P<id_parti>[0-9]+)', views.partiMembres, name='partiMembres'),
	url(r'^partiPublications/(?P<id_parti>[0-9]+)', views.partiPublications, name='partiPublications'),	
	url(r'^partiTravaux/(?P<id_parti>[0-9]+)', views.partiTravaux, name='partiTravaux'),	
	
	url(r'^travauxListe', views.travauxListe, name='travauxListe'),
		
	url(r'^userPresentation/(?P<id_user>[0-9]+)', views.userPresentation, name='userPresentation'),	
		
	url(r'^cellule_accueil', views.cellule_accueil, name='cellule_accueil'),
	url(r'^cellule_presentation/(?P<id_cellule>[0-9]+)', views.cellule_presentation, name='cellule_presentation'),
]