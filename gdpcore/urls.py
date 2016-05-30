from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
	
	url(r'^init', views.index, name='init'),
	
	url(r'^selection_cycle', views.selection_cycle, name='selection_cycle'),
	url(r'^tobedone', views.tobedone, name='tobedone'),
	url(r'^selection_graph', views.selection_graph, name='selection_graph'),
	url(r'^proposition_browser/(?P<id_prop>[0-9]+)', views.proposition_browser, name='proposition_browser'),

	url(r'^link_browser/(?P<id_link>[0-9]+)', views.link_browser, name='link_browser'),
	url(r'^link_attack/(?P<id_link>[0-9]+)', views.link_attack, name='link_attack'),
	url(r'^precision_request/(?P<id_prop>[0-9]+)', views.precision_request, name='precision_request'),
	url(r'^supplement_request/(?P<id_prop>[0-9]+)', views.supplement_request, name='supplement_request'),
	url(r'^attention_request/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.attention_request, name='attention_request'),
	url(r'^text_request/(?P<id_prop>[0-9]+)', views.text_request, name='text_request'),
	url(r'^new_proposition/(?P<id_prop>[0-9]+)', views.new_proposition, name='new_proposition'),
	url(r'^new_link/(?P<id_prop>[0-9]+)', views.new_link, name='new_link'),
	url(r'^edit_proposition/(?P<id_prop>[0-9]+)', views.edit_proposition, name='edit_proposition'),
	url(r'^new_cycle', views.new_cycle, name='new_cycle'),
	url(r'^new_starting_proposition', views.new_starting_proposition, name='new_starting_proposition'),
	url(r'^similar_propositions', views.similar_propositions, name='similar_propositions'),
	url(r'^notif_viewer/(?P<id_notif>[0-9]+)', views.notif_viewer, name='notif_viewer'),
	url(r'^tag_generator', views.tag_generator, name='tag_generator'),
	
	url(r'^search_proposition', views.search_proposition, name='search_proposition'),
	url(r'^envir_viewer/(?P<id_prop>[0-9]+)', views.envir_viewer, name='envir_viewer'),
	url(r'^env_viewer/(?P<id_prop>[0-9]+)', views.env_viewer, name='env_viewer'),
	
	url(r'^super_viewer/(?P<id_prop>[0-9]+)', views.super_viewer, name='super_viewer'),
	
	
	url(r'^sv_addprop/(?P<id_prop>[0-9]+)/(?P<id_link>[0-9]+)', views.sv_addprop, name='sv_addprop'),
	url(r'^save_graph', views.save_graph, name='save_graph'),
	url(r'^graph_viewer/(?P<id_graph>[0-9]+)', views.graph_viewer, name='graph_viewer'),
	url(r'^incremental_viewer/(?P<id_prop>[0-9]+)', views.incremental_viewer, name='incremental_viewer'),
	url(r'^final_viewer/(?P<id_graph>[0-9]+)', views.final_viewer, name='final_viewer'),

	url(r'^ajax_propenvir/(?P<id_prop>[0-9]+)', views.ajax_propenvir, name='ajax_propenvir'),
	url(r'^ajax_getcomments/(?P<id_prop>[0-9]+)', views.ajax_getcomments, name='ajax_getcomments'),
	url(r'^ajax_newanswer', views.ajax_newanswer, name='ajax_newanswer'),
	url(r'^ajax_newcomment', views.ajax_newcomment, name='ajax_newcomment'),
	url(r'^ajax_editprop', views.ajax_editprop, name='ajax_editprop'),
	url(r'^ajax_newprop', views.ajax_newprop, name='ajax_newprop'),
	url(r'^ajax_connect', views.ajax_connect, name='ajax_connect'),
	url(r'^ajax_linkattack', views.ajax_linkattack, name='ajax_linkattack'),
	url(r'^ajax_linkremove', views.ajax_linkremove, name='ajax_linkremove'),
	url(r'^ajax_quicksave', views.ajax_quicksave, name='ajax_quicksave'),	
	url(r'^new_graph', views.new_graph, name='new_graph'),	
	
	url(r'^register', views.register, name='register'),	
	
	url('^', include('django.contrib.auth.urls')),
]