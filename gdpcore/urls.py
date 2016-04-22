from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
	url(r'^selection_cycle', views.selection_cycle, name='selection_cycle'),
	url(r'^tobedone', views.tobedone, name='tobedone'),
	url(r'^graph_browser/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.graph_browser, name='graph_browser'),
	url(r'^graph_browser_free/(?P<id_prop>[0-9]+)', views.graph_browser_free, name='graph_browser_free'),
	url(r'^link_browser/(?P<id_cycle>[0-9]+)/(?P<id_link>[0-9]+)', views.link_browser, name='link_browser'),
	url(r'^link_attack/(?P<id_cycle>[0-9]+)/(?P<id_link>[0-9]+)', views.link_attack, name='link_attack'),
	url(r'^precision_request/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.precision_request, name='precision_request'),
	url(r'^supplement_request/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.supplement_request, name='supplement_request'),
	url(r'^attention_request/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.attention_request, name='attention_request'),
	url(r'^text_request/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.text_request, name='text_request'),
	url(r'^new_proposition/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.new_proposition, name='new_proposition'),
	url(r'^new_link/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.new_link, name='new_link'),
	url(r'^edit_proposition/(?P<id_cycle>[0-9]+)/(?P<id_prop>[0-9]+)', views.edit_proposition, name='edit_proposition'),
	url(r'^new_cycle', views.new_cycle, name='new_cycle'),
	url(r'^new_starting_proposition', views.new_starting_proposition, name='new_starting_proposition'),
	url(r'^similar_propositions', views.similar_propositions, name='similar_propositions'),
	url(r'^notif_viewer/(?P<id_notif>[0-9]+)', views.notif_viewer, name='notif_viewer'),
	url(r'^tag_generator', views.tag_generator, name='tag_generator'),
	
	url(r'^search_proposition', views.search_proposition, name='search_proposition'),
	
	url('^', include('django.contrib.auth.urls')),
]