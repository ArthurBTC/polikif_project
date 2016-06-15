from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Proposition, LinkType, Link, Cycle, Comment, Notification, Implication, Graph, Elemgraph, CommentGraph, Show, ShowPart
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from difflib import SequenceMatcher
from django.core import serializers
import json
import requests
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime  

def theater(request, id_show):
	show = Show.objects.get(pk=id_show)
	showparts = ShowPart.objects.filter(show = show)
	return render(request,'gdpcore/theater.html',{'show': show, 'showparts':showparts });

def esAddProp(request):
	
	indexname = 'newindex'

	mapping_json = json.dumps(	
		{
		  "mappings": {
			"proposition" : {
			  "properties" : {
				"text" : {
				  "type" :    "string",
				  "analyzer": "french"
				},
				"user_id" : {
				  "type" :   "long"
				}
			  }
			}
		  }
		}
	)
	
	r = requests.put('http://localhost:9200/'+indexname, mapping_json)
	
	props = Proposition.objects.all()
	
	for prop in props:
		data =  {					
					"text":   prop.text,
					"user_id": prop.autor.pk 
				}	
	
		data_json = json.dumps(data)	
	
		r = requests.put('http://localhost:9200/'+indexname+'/proposition/'+str(prop.pk), data_json)
		
		
	return HttpResponse(r)
	
@csrf_exempt	
def getSimil(request):

	# j = json.loads(request.body.decode('utf-8'))
	
	data =  {	
				"query": { "match": { "text": request.POST["text"] } }
			}	

	data_json = json.dumps(data)	
	
	r = requests.post('http://localhost:9200/newindex/proposition/_search', data_json)
	
	
	return JsonResponse( r.json() )
	

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/books/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
	
def index(request):
	return render(request,'gdpcore/index.html')
	
#Pour la selection des cycles :
@login_required
def selection_cycle(request):

	cycles = Cycle.objects.all().order_by('-last_prop_date')
	return render(request,'gdpcore/selection_cycle.html',{'cycles' : cycles})

#Visualisation des choses à faire
@login_required
def tobedone(request):
	notifs = notifs = Notification.objects.filter(autor = request.user).order_by('-creation_date')

	props_precison = Proposition.objects.filter(autor = request.user).filter(demande_precision = True)
	props_supplement = Proposition.objects.filter(autor = request.user).filter(demande_supplement = True)
	
	last_props = Proposition.objects.filter(autor = request.user).order_by('-creation_date')
	
	return render(request,'gdpcore/tobedone.html',{'props_precison' : props_precison,'props_supplement' : props_supplement, 'notifs' : notifs, 'last_props':last_props})

	
	
def proposition_browser(request, id_prop):
	
	main_prop = Proposition.objects.get(id = id_prop)
	nav_props = Proposition.objects.filter(cycle = main_prop.cycle).order_by('-creation_date')[:3]
	comments = Comment.objects.filter(proposition__id = id_prop).order_by('creation_date')
	
	links_right = Link.objects.filter(left_prop = main_prop)
	links_left = Link.objects.filter(right_prop = main_prop)
	
	return render(request,'gdpcore/proposition_browser.html',{'id_prop': id_prop,
														'nav_props': nav_props, 
														'main_prop': main_prop, 
														'comments': comments,
														'links_right': links_right, 'links_left': links_left })
	
	
	
def link_browser(request, id_link):
	main_link = Link.objects.get(id = id_link)
	implications = Implication.objects.filter(link = main_link)
	return render(request,'gdpcore/link_browser.html',{'main_link': main_link, 'implications': implications})
	
def precision_request(request, id_prop):
	prop = Proposition.objects.get(id = id_prop)
	prop.demande_precision = True
	prop.save()
	
	add_comment(request.user, prop, 'DP', 'a ouvert une demande une précision')
	
	autors = Comment.objects.filter(proposition = prop).values('autor')
	myList =[]
	for autor in autors:
		myList.append(autor['autor'])
	myNewList = list(set(myList))
	
	for usrid in myNewList:
		if usrid != request.user.id:
			generate_notification(User.objects.get(id=usrid), prop, 'DP')
			
	cycle_updater(prop.cycle.id)
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))
	
def supplement_request(request, id_prop):
	prop = Proposition.objects.get(id = id_prop)
	prop.demande_supplement = True
	prop.save()
	
	add_comment(request.user, prop, 'DS', 'a ouvert une demande de source')
	
	autors = Comment.objects.filter(proposition = prop).values('autor')
	myList =[]
	for autor in autors:
		myList.append(autor['autor'])
	myNewList = list(set(myList))
	
	for usrid in myNewList:
		if usrid != request.user.id:
			generate_notification(User.objects.get(id=usrid), prop, 'DS')
	
	cycle_updater(prop.cycle.id)
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))
	
def attention_request(request, id_prop):
	prop = Proposition.objects.get(id = id_prop)
	prop.demande_attention = True
	prop.save()
	
	add_comment(request.user, prop, "Demande d'attention", "demande de l'attention")
	
	generate_notification(prop.autor, prop, 'DA')
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))
	
	
def text_request(request, id_prop):
	prop = Proposition.objects.get(id = id_prop)
	
	add_comment(request.user, prop, 'TX', request.POST['reponse'])	
	
	autors = Comment.objects.filter(proposition = prop).values('autor')
	for autor in autors:
		usr = User.objects.get(id=autor['autor'])
		if usr.id != request.user.id:
			generate_notification(usr, prop, 'NC')

	cycle_updater(prop.cycle.id)
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))

	
def add_comment(autor, prop, nature, text):
	comment = Comment(autor = autor,
					  nature = nature,
					  text = text,
					  creation_date = datetime.now(),
					  proposition = prop
						)
	comment.save()
	return comment
	
def generate_notification(aut, prop, nat):
	
	notif = Notification(autor = aut,
						proposition = prop,
						nature = nat,
						creation_date = datetime.now(),
						modification_date = datetime.now(),
						viewed = False
						)
	notif.save()				
						
def notif_viewer(request, id_notif):
	notif = Notification.objects.get(id = id_notif)
	notif.viewed = True
	notif.save()
	
	id_cycle = 1
	id_prop = notif.proposition.id
	
#A CORRIGER ATTENTIOn	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))


						
#Ajout d'une proposition depuis le modal	
def new_proposition(request, id_prop):
	
	initial_prop = Proposition.objects.get(id=id_prop)
	
	prop = Proposition(autor = request.user,
				text = request.POST['newprop'],
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				cycle = initial_prop.cycle,
				nature = 'Diagnostic',
				trafic = 0,
				demande_precision = False,
				demande_supplement = False,
				demande_attention = False
				)
	prop.save()
	
	if request.POST['optionsRadios'] == 'donc':
		nat = 'Donc'
		left = initial_prop
		right = prop
	elif request.POST['optionsRadios'] == 'car':
		nat = 'Donc'
		right = initial_prop
		left = prop
	elif request.POST['optionsRadios'] == 'ex':
		nat = 'Exemple'
		left = initial_prop
		right = prop
	elif request.POST['optionsRadios'] == 'ccr':
		nat = 'Concurrence'
		left = initial_prop
		right = prop
		
	
	link = Link(autor = request.user,
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				nature = nat,
				cycle = initial_prop.cycle,
				trafic = 0,
				left_prop = left,
				right_prop = right,
				junction = 'No'				
				)

	link.save()
	
	if prop.autor.id != initial_prop.autor.id:	
#		notif = Notification.objects.filter(autor = initial_prop.autor).filter(prop = initial_prop).filter(viewed = False).first()	
#		if notif != None:
		generate_notification(initial_prop.autor, initial_prop, 'NL')
#		else:
#			notif.modification_date = datetime.now()
			
	add_comment(prop.autor, prop, 'TX', 'Proposition créée : '+prop.text)
	
	cycle_updater(initial_prop.cycle.id)
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))
	
def new_link(request, id_prop):
	
	initial_prop = Proposition.objects.get(id=id_prop)
	prop = Proposition.objects.get(id=int(request.POST['second_prop']))

	if request.POST['optionsRadios'] == 'donc':
		nat = 'Donc'
		left = initial_prop
		right = prop
	elif request.POST['optionsRadios'] == 'car':
		nat = 'Donc'
		right = initial_prop
		left = prop
	elif request.POST['optionsRadios'] == 'ex':
		nat = 'Exemple'
		left = initial_prop
		right = prop
	elif request.POST['optionsRadios'] == 'ccr':
		nat = 'Concurrence'
		left = initial_prop
		right = prop
		
	link = Link(autor = request.user,
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				nature = nat,
				cycle = initial_prop.cycle,
				trafic = 0,
				left_prop = left,
				right_prop = right,
				junction = 'No'				
				)
	link.save()
	
	if link.autor.id != initial_prop.autor.id:	
#		notif = Notification.objects.filter(autor = initial_prop.autor).filter(prop = initial_prop).filter(viewed = False).first()	
#		if notif != None:
		generate_notification(initial_prop.autor, initial_prop, 'NL')
#		else:
#			notif.modification_date = datetime.now()

	if link.autor.id != prop.autor.id:
		generate_notification(prop.autor, prop, 'NL')
	
	cycle_updater(initial_prop.cycle.id)
	
	return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))	
	
#Edition d'une proposition depuis le modal	
def edit_proposition(request, id_prop):
	if request.method == 'POST':
		prop = Proposition.objects.get(id = id_prop)

		#On change le texte
		prop.text = request.POST['edit']
		prop.demande_precision = False
		prop.save()
		
		#On voit les liens qui sont connectés, et on les met en suspension
		lefts = Link.objects.filter(left_prop__id = id_prop).exclude(autor = prop.autor)
		rights = Link.objects.filter(right_prop__id = id_prop).exclude(autor = prop.autor)
		
		for left in lefts:
			left.status = 'P'
			left.save()
			
		
		for right in rights:
			right.status = 'P'
			right.save()
		
		#On prévient tout le monde que la proposition a été changée:
		autors = Comment.objects.filter(proposition = prop).values('autor')
		myList =[]
		for autor in autors:
			myList.append(autor['autor'])
		myNewList = list(set(myList))
		
		for usrid in myNewList:
			if usrid != request.user.id:
				generate_notification(User.objects.get(id=usrid), prop, 'MP')
	
		add_comment(prop.autor, prop, 'MP', 'Modification de la proposition : '+prop.text)			
		
		cycle_updater(prop.cycle.id)
		
		return HttpResponseRedirect(reverse('proposition_browser', args=(id_prop,)))
			

	
def new_cycle(request):
	if request.method == 'POST':
		cycle = Cycle(autor = request.user,
					text = request.POST['description'],
					creation_date = datetime.now(),
					proposition_initiale = request.POST['prop_ini'],
					last_prop_date = datetime.now()
					)
		cycle.save()
		
		return HttpResponseRedirect(reverse('selection_cycle'))

	
	props = Proposition.objects.all()
	return render(request,'gdpcore/new_cycle.html',{'props':props})
	
	
def new_starting_proposition(request):
	if request.method == 'POST':
		cycle = Cycle(autor = request.user,
					text = request.POST['description'],
					creation_date = datetime.now(),
					last_prop_date = datetime.now(),
					proposition_initiale = 0					
					)
		cycle.save()
		
		prop = Proposition(autor = request.user,
						text = request.POST['proposition'],
						creation_date = datetime.now(),
						modification_date = datetime.now(),
						cycle = cycle,
						nature = 'Diagnostic',
						trafic = 0,
						demande_precision = False,
						demande_supplement = False,
						demande_attention = False,
						simil = 0					
						)
		
		prop.save()
		
		cycle.proposition_initiale = prop.id
		cycle.save()
		
		return HttpResponseRedirect(reverse('selection_cycle'))

	
	props = Proposition.objects.all()
	return render(request,'gdpcore/new_cycle.html',{'props':props})		
		
		
def link_attack(request, id_link):
	if request.method == 'POST':
	
		main_link = Link.objects.get(id = id_link)

		prop_imp = Proposition(autor = User.objects.get(username = 'nobody'),
					text = request.POST['implication'],
					creation_date = datetime.now(),
					modification_date = datetime.now(),
					cycle = main_link.cycle,
					nature = 'Diagnostic',
					trafic = 0,
					demande_precision = False,
					demande_supplement = False,
					demande_attention = False				
					)
		
		prop_imp.save()
	
		implication = Implication(autor = request.user,
								proposition = prop_imp,
								link = main_link,
								creation_date = datetime.now()
								)
		implication.save()
		
		prop_ccr = Proposition(autor = request.user,
					text = request.POST['attack'],
					creation_date = datetime.now(),
					modification_date = datetime.now(),
					cycle = main_link.cycle,
					nature = 'Diagnostic',
					trafic = 0,
					demande_precision = False,
					demande_supplement = False,
					demande_attention = False				
					)
		
		prop_ccr.save()
		
		link = Link(autor = request.user,
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				nature = 'Concurrence',
				cycle = main_link.cycle,
				trafic = 0,
				left_prop = prop_ccr,
				right_prop = prop_imp,
				junction = 'No'				
				)

		link.save()
		
		generate_notification(main_link.autor, prop_imp, 'CL')
		
		cycle_updater(main_link.cycle.id)
		
		return HttpResponseRedirect(reverse('link_browser', args=(id_link,)))

def cycle_updater(id_cycle):
	cycle = Cycle.objects.get(id = id_cycle)
	props_cycle = Proposition.objects.filter(cycle = cycle)
	cycle.nb = props_cycle.count()
	if props_cycle:
		cycle.last_prop_date = datetime.now()
	cycle.save()

def tag_generator(request):

	cycles = Cycle.objects.all()
	for cycle in cycles:
		props_cycle = Proposition.objects.filter(cycle = cycle)
		cycle.nb = props_cycle.count()
		if props_cycle:
			cycle.last_prop_date = props_cycle.order_by('-creation_date')[0].creation_date
		cycle.save()

	props = Proposition.objects.all()
	for prop in props:			
		place = prop.text
		place = place.replace("c'", "")
		place = place.replace("l'", "")
		place = place.replace("n'", "")
		place = place.replace("d'", "")
		place = place.replace("C'", "")
		place = place.replace("L'", "")
		place = place.replace("N'", "")
		place = place.replace("D'", "")
		place = place.replace(",", "")
		place = place.replace(".", "")
		place = place.replace("!", "")
		
		noise_words_set = {'ma', 'ta', 'sa', 'mon', 'ton','son','qui','que',
		'quoi','dont','ou','mais','ou','et','donc','or','ni','car','la',
		'le','les','notre','votre','leur','nos','vos','leur','ce','ces',
		'cette','cet','un','une','des','du','ne','à','se','me','te','pas',
		'tout','en','a','avec','sans','de','mes','tes','ses','pour','y','plus','moins',
		'je','tu','il','elle','on','nous','vous','ils','elles','eux','au','a','où','par','tous'}
		
		stuff = [' '.join(w for w in place.split() if w.lower() not in noise_words_set)]
		prop.tags = stuff[0]
		prop.save()
		

				
	return HttpResponseRedirect(reverse('selection_cycle'))

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
	
def similar_propositions(request):
	if request.method == 'POST':
		
		place = request.POST['parameter']
		place = place.replace("c'", "")
		place = place.replace("l'", "")
		place = place.replace("n'", "")
		place = place.replace("d'", "")
		place = place.replace("C'", "")
		place = place.replace("L'", "")
		place = place.replace("N'", "")
		place = place.replace("D'", "")
		place = place.replace(",", "")
		place = place.replace(".", "")
		place = place.replace("!", "")
		
		noise_words_set = {'ma', 'ta', 'sa', 'mon', 'ton','son','qui','que',
		'quoi','dont','ou','mais','ou','et','donc','or','ni','car','la',
		'le','les','notre','votre','leur','nos','vos','leur','ce','ces',
		'cette','cet','un','une','des','du','ne','à','se','me','te','pas',
		'tout','en','a','avec','sans','de','mes','tes','ses','pour','y','plus','moins',
		'je','tu','il','elle','on','nous','vous','ils','elles','eux','au','a','où','par','tous'}
		
		stuff = [' '.join(w for w in place.split() if w.lower() not in noise_words_set)]
		
		tags = stuff[0]			
		props = Proposition.objects.all()
		
		for prop in props:
			n = 0
			words1 = set(tags.split())
			for word in prop.tags.split():
	#			if word in words1:
	#				n += 1
				for word1 in words1:
					if similar(word1,word) > 0.5:
						n = n + 1	
			prop.simil = n
			prop.save()
		
		props = Proposition.objects.order_by('-simil')[:10]		
			
		return render(request,'gdpcore/similar_propositions.html',{'props': props, 'text': request.POST['parameter']})
		
def search_proposition(request):
	props = Proposition.objects.all()
	return render(request,'gdpcore/search_proposition.html',{'props': props})
	
def envir_viewer(request, id_prop):

	main_prop = Proposition.objects.get(id=id_prop)
	links_right = Link.objects.filter(left_prop = main_prop)
	links_left = Link.objects.filter(right_prop = main_prop)
	
	all_links = {}
		
	for link in links_left:
		all_links[str(link.id)] = link
		
		more_links = Link.objects.filter(left_prop = link.right_prop)
		for more_link in more_links:
			all_links[str(more_link.id)] = more_link

		more_links = Link.objects.filter(right_prop = link.right_prop)
		for more_link in more_links:
			all_links[str(more_link.id)] = more_link			
		

	for link in links_right:
		all_links[str(link.id)] = link
		
		more_links = Link.objects.filter(left_prop = link.left_prop)
		for more_link in more_links:
			all_links[str(more_link.id)] = more_link

		more_links = Link.objects.filter(right_prop = link.left_prop)
		for more_link in more_links:
			all_links[str(more_link.id)] = more_link
			
	return render(request,'gdpcore/envir_viewer.html',{'main_prop':main_prop,'all_links':all_links})
	
def env_viewer(request, id_prop):

	main_prop = Proposition.objects.get(id=id_prop)
	
	ccrs1 = Link.objects.filter(left_prop = main_prop).filter(nature = 'Concurrence')
	ccrs2 = Link.objects.filter(right_prop = main_prop).filter(nature = 'Concurrence')
	
	cars = {}
	for ccr1 in ccrs1:
		cars[str(ccr1.id)]= Link.objects.filter(left_prop = ccr1.right_prop).filter(nature = 'Donc')
	for ccr2 in ccrs2:
		cars[str(ccr2.id)]= Link.objects.filter(left_prop = ccr2.left_prop).filter(nature = 'Donc')
		
	doncs = {}
	for ccr1 in ccrs1:
		doncs[str(ccr1.id)]= Link.objects.filter(right_prop = ccr1.right_prop).filter(nature = 'Donc')
	for ccr2 in ccrs2:
		doncs[str(ccr2.id)]= Link.objects.filter(right_prop = ccr2.left_prop).filter(nature = 'Donc')

			
	return render(request,'gdpcore/env_viewer.html',{'main_prop':main_prop,'ccrs1':ccrs1,'ccrs2':ccrs2,'cars':cars,'doncs':doncs})
	
	
def super_viewer(request, id_prop):

	main_prop = Proposition.objects.get(id = id_prop)
	links_right = Link.objects.filter(left_prop = main_prop)
	links_left = Link.objects.filter(right_prop = main_prop)
	
	return render(request,'gdpcore/super_viewer.html',{'main_prop': main_prop, 'links_right': links_right, 'links_left': links_left })
	
def sv_addprop(request, id_prop, id_link):
#	link = Link.objects.get(id = id_link)
#	prop_ini = Proposition.objects.get(id = id_prop)
	
#	if link.left_prop == prop_ini:
#		prop = link.right_prop
#	elif link.right_prop == prop_ini:
#		prop = link.left_prop
		
#	links_left = Link.objects.filter(left_prop = prop)
#	links_right = Link.objects.filter(right_prop = prop)
	
#	all_objects = list([link]) + list([prop]) + list(links_left) + list(links_right)
#	data = serializers.serialize('json', all_objects)

	main_prop = Proposition.objects.get(id = id_prop)
	if id_link != '0':
		main_link = Link.objects.get(id = id_link)
		if main_prop == main_link.left_prop:
			link_sens = 0
		else:
			link_sens = 1
	else:
		main_link=None;
		link_sens=None;
	links_right = Link.objects.filter(left_prop = main_prop)
	links_left = Link.objects.filter(right_prop = main_prop)
	
	props = []
	
	for link_right in links_right:
		props.append(link_right.right_prop)
		
	for link_left in links_left:
		props.append(link_left.left_prop)
	
	all_objects = list([main_prop])+list([main_link])+list(links_right)+list(links_left)+props
	data = serializers.serialize('json', all_objects)
#	return render(request,'gdpcore/sv_addprop.html',{'main_prop': main_prop, 'main_link': main_link, 'links_right': links_right, 'links_left': links_left, 'link_sens': link_sens })
	return HttpResponse(data)
	

	
def incremental_viewer(request, id_prop):

	main_prop = Proposition.objects.get(id = id_prop)

	
	return render(request,'gdpcore/incremental_viewer.html',{'main_prop': main_prop })

@login_required
def final_viewer(request, id_graph):
	graph = Graph.objects.get(id = id_graph)
	comments_graph = CommentGraph.objects.filter(graph = graph)
	
	elems = Elemgraph.objects.filter(graph = graph)

	props = []
	links = []
	implications = []
	attributes = {}
	for elem in elems:
		if elem.displayed == True:
			attributes[elem.proposition.id] = {'x':elem.x,'y':elem.y}
			
			props.append(elem.proposition)
			
			links_right = Link.objects.filter(left_prop = elem.proposition)
			links_left = Link.objects.filter(right_prop = elem.proposition)
				
			
				
			for link_right in links_right:
				links.append(link_right)
				props.append(link_right.right_prop)
				
				imps = Implication.objects.filter(link = link_right)
				for imp in imps:
					implications.append(imp)
					props.append(imp.proposition)
				
			for link_left in links_left:
				links.append(link_left)
				props.append(link_left.left_prop)
				
				imps = Implication.objects.filter(link = link_left)
				for imp in imps:
					implications.append(imp)
					props.append(imp.proposition)				
				
			props = list(set(props))
			links = list(set(links))
	
	link_types = LinkType.objects.all()
	json_linktypes = serializers.serialize('json', link_types)
	
	return render(request,'gdpcore/final_viewer3.html',{
					'graph': graph,
					'link_types': link_types,
					'json_linktypes': json_linktypes,
					'props': props,
					'attributes': attributes, 
					'links':links,
					'implications': implications,
					'comments_graph': comments_graph})
	
def ajax_propenvir(request, id_prop):

	main_prop = Proposition.objects.get(id = id_prop)
	links_right = Link.objects.filter(left_prop = main_prop)
	links_left = Link.objects.filter(right_prop = main_prop)
	props = []
	authorList = [];
	for link_right in links_right:
		props.append(link_right.right_prop)
		authorList.append(link_right.autor)
		authorList.append(link_right.right_prop.autor)
		
	for link_left in links_left:
		props.append(link_left.left_prop)
		authorList.append(link_left.autor)
		authorList.append(link_left.left_prop.autor)
		
	authorList = list(set(authorList))
		
	all_objects = list([main_prop])+list(links_right)+list(links_left)+props+authorList
	data = serializers.serialize('json', all_objects)
		
	return HttpResponse(data)
	
	
@csrf_exempt
def save_graph(request):
	if request.method == 'POST':	

		j = json.loads(request.body.decode('utf-8'))
		
		graph, created = Graph.objects.update_or_create(
				title = j['title'],
				autor = request.user,
				defaults = {
					'graphstring': j['graph'],
					'creation_date':datetime.now(),
					'originx':j['origin']['x'] ,
					'originy':j['origin']['y'] 			
					}	
				)
	
	for cell in j['graph']['cells']:
		if cell["type"] == "basic.TextBlock":
			if cell['attrs']['.']['display'] == 'none':
				display = False
			else:
				display = True
			
			elem, created = Elemgraph.objects.update_or_create(
					graph=graph, 
					proposition = Proposition.objects.get(id = cell['id_prop']), 
					defaults={
						'x': cell['position']['x'],
						'y': cell['position']['y'],
						'displayed':display
						})
						
		if cell["type"] == "basic.twoTextRect":
			if cell['attrs']['.']['display'] == 'none':
				display = False
			else:
				display = True
			
			elem, created = Elemgraph.objects.update_or_create(
					graph=graph, 
					proposition = Proposition.objects.get(id = cell['id_prop']), 
					defaults={
						'x': cell['position']['x'],
						'y': cell['position']['y'],
						'displayed':display
						})

	return HttpResponse('OK')

	
def graph_viewer(request, id_graph):
	graph = Graph.objects.get(id = id_graph)

	j = json.loads(graph.graphstring)['cells']
	
	id_props =[]
	id_links=[]
	props={}
	links={}
	
	for cell in j:
		if 'id_prop' in cell:
			id_props.append(cell['id_prop'])
		if 'id_link' in cell:
			id_links.append(cell['id_link'])

	for id_prop in id_props:
		main_prop = Proposition.objects.get(id = id_prop)
		prop = {}
		prop['main_prop']= main_prop
		prop['links_right']= Link.objects.filter(left_prop = main_prop)
		prop['links_left']= Link.objects.filter(right_prop = main_prop)
		props[id_prop] = prop
	
	
	return render(request,'gdpcore/graph_viewer.html',{'graph': graph, 'j':props})
	
def selection_graph(request):
	from django.db.models import Count
	graphs = Graph.objects.order_by('-creation_date')
	return render(request,'gdpcore/selection_graph.html',{'graphs': graphs})
	
@csrf_exempt	
def ajax_newanswer(request):
	
	initial_prop = Proposition.objects.get(id=request.POST['id_prop'])
	
	
	if request.POST['nature'] == 'diagnostic':
	
		prop = Proposition(autor = request.user,
					text = request.POST['newprop'],
					creation_date = datetime.now(),
					modification_date = datetime.now(),
					cycle = initial_prop.cycle,
					nature = 'Diagnostic',
					trafic = 0,
					demande_precision = False,
					demande_supplement = False,
					demande_attention = False
					)
					
	elif request.POST['nature'] == 'youtube':
		
		prop = Proposition(
					autor = request.user,
					text = request.POST['youtubeTitle'],
					creation_date = datetime.now(),
					modification_date = datetime.now(),
					cycle = initial_prop.cycle,
					nature = 'YT',
					ytid = request.POST['youtubeId'],
					videoBeginning = int(request.POST['youtubeBegin']),
					videoEnd = int(request.POST['youtubeEnd'])	

					)			
					
	prop.save()
	
	if request.POST['nature'] == 'diagnostic':
		linktype = LinkType.objects.get(id = request.POST['type_id'])	
	
	elif request.POST['nature'] == 'youtube':
		linktype = LinkType.objects.get(type = 'exemple')
	
	if linktype.sens == True:
		nat = linktype.inverse
		left = prop
		right = initial_prop
		linktype = LinkType.objects.get(type = linktype.inverse)
		
	else:
		nat = linktype.type
		left = initial_prop
		right = prop
	
	
	link = Link(autor = request.user,
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				nature = nat,
				type = linktype,
				cycle = initial_prop.cycle,
				trafic = 0,
				left_prop = left,
				right_prop = right,
				junction = 'No'				
				)

	link.save()
	
	if prop.autor.id != initial_prop.autor.id:	
		generate_notification(initial_prop.autor, initial_prop, 'NL')
			
	add_comment(prop.autor, prop, 'TX', 'Proposition créée : '+prop.text)
	
	cycle_updater(initial_prop.cycle.id)
	
	return JsonResponse(serializers.serialize('json', [prop,link]), safe = False)
	
def ajax_getcomments(request, id_prop):

	comments = Comment.objects.filter(proposition__id = id_prop).order_by('creation_date')
	return JsonResponse(serializers.serialize('json', comments), safe = False)
	
@csrf_exempt	
def ajax_newcomment(request):
	
	prop = Proposition.objects.get(id = request.POST['id_prop'])
	comment = add_comment(request.user, prop, 'TX', request.POST['comment_text'])
	
	autors = Comment.objects.filter(proposition = prop).values('autor')
	for autor in autors:
		usr = User.objects.get(id=autor['autor'])
		if usr.id != request.user.id:
			generate_notification(usr, prop, 'NC')

	cycle_updater(prop.cycle.id)	
	
	return JsonResponse(serializers.serialize('json', [comment]), safe = False)

@csrf_exempt	
def ajax_editprop(request):

	id_prop = request.POST['id_prop']
	prop = Proposition.objects.get(id=id_prop)

	#On change le texte
	prop.text = request.POST['edit_prop']
	prop.demande_precision = False
	prop.save()

	#On voit les liens qui sont connectés, et on les met en suspension
	lefts = Link.objects.filter(left_prop__id = id_prop).exclude(autor = prop.autor)
	rights = Link.objects.filter(right_prop__id = id_prop).exclude(autor = prop.autor)
	
	for left in lefts:
		left.status = 'P'
		left.save()
			
	for right in rights:
		right.status = 'P'
		right.save()

	#On prévient tout le monde que la proposition a été changée:
	autors = Comment.objects.filter(proposition = prop).values('autor')
	myList =[]
	for autor in autors:
		myList.append(autor['autor'])
	myNewList = list(set(myList))
	
	for usrid in myNewList:
		if usrid != request.user.id:
			generate_notification(User.objects.get(id=usrid), prop, 'MP')

	add_comment(prop.autor, prop, 'MP', 'Modification de la proposition : '+prop.text)			
	
	cycle_updater(prop.cycle.id)

	all_items = list([prop]) + list(lefts) + list(rights)
	return JsonResponse(serializers.serialize('json', all_items), safe = False)
	# return HttpResponse('lala')

@csrf_exempt	
def ajax_newprop(request):

	if request.POST['nature'] == 'diagnostic':	
		prop = Proposition(
			autor = request.user,
			text = request.POST['newprop'],		
			creation_date = datetime.now(),
			modification_date = datetime.now(),
			cycle = Cycle.objects.get(pk=1)
			)
	
	elif request.POST['nature'] == 'youtube':
		prop = Proposition(
			autor = request.user,
			text = request.POST['youtubeTitle'],		
			creation_date = datetime.now(),
			modification_date = datetime.now(),
			cycle = Cycle.objects.get(pk=1),
			
			nature = 'YT',
			ytid = request.POST['youtubeId'],
			videoBeginning = int(request.POST['youtubeBegin']),
			videoEnd = int(request.POST['youtubeEnd'])
			)
		
	prop.save()
	
	all_items = list([prop])
	return JsonResponse(serializers.serialize('json', all_items), safe = False)	

@csrf_exempt	
def ajax_connect(request):

	initial_prop = Proposition.objects.get(pk = request.POST['left_prop'])
	prop = Proposition.objects.get(pk = request.POST['right_prop'])

	linktype = LinkType.objects.get(id = request.POST['type_id'])	
	
	if linktype.sens == True:
		nat = linktype.inverse
		left = prop
		right = initial_prop
		linktype = LinkType.objects.get(type = linktype.inverse)
		
	else:
		nat = linktype.type
		left = initial_prop
		right = prop	

	link = Link(
		autor = request.user,
		creation_date = datetime.now(),
		modification_date = datetime.now(),
		nature = nat,
		type = linktype,
		cycle = Cycle.objects.get(pk=1),		
		left_prop = left,
		right_prop = right	
		)
		
	link.save()
	all_items = list([link])
	return JsonResponse(serializers.serialize('json', all_items), safe = False)	

@csrf_exempt
def ajax_linkattack(request):

	main_link = Link.objects.get(id = request.POST['id_link'])

	propImplication = Proposition(autor = User.objects.get(username = 'nobody'),
				text = request.POST['linkImplication'],
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				cycle = main_link.cycle,
				nature = 'Diagnostic',				
				)
	propImplication.save()
	
	implication = Implication(autor = request.user,
						proposition = propImplication,
						link = main_link,
						creation_date = datetime.now()
					)
	implication.save()	

	prop_ccr = Proposition(autor = request.user,
				text = request.POST['linkAttack'],
				creation_date = datetime.now(),
				modification_date = datetime.now(),
				cycle = main_link.cycle,
				nature = 'Diagnostic',				
				)
	
	prop_ccr.save()

	link = Link(autor = request.user,
			creation_date = datetime.now(),
			modification_date = datetime.now(),
			nature = 'Concurrence',
			cycle = main_link.cycle,
			left_prop = prop_ccr,
			right_prop = propImplication,			
			)

	link.save()	

	generate_notification(main_link.autor, propImplication, 'CL')
	cycle_updater(main_link.cycle.id)
	
	all_items = list([main_link]) + list([propImplication]) + list([implication]) + list([prop_ccr])+ list([link])
	return JsonResponse(serializers.serialize('json', all_items), safe = False)		
	
@csrf_exempt	
def ajax_linkremove(request):

	main_link = Link.objects.get(id = request.POST['id_link'])	
	main_link.delete();
	return HttpResponse('')

@csrf_exempt	
def ajax_quicksave(request):
	
	if request.method == 'POST':	
		
		graph = Graph.objects.get(id = request.POST['id_graph'])
		
		graph.graphstring = request.POST['graphstring']
		graph.creation_date = datetime.now()
		graph.originx = request.POST['x']
		graph.originy = request.POST['y']
		
		j = json.loads(request.POST['graphstring'])
		
		graph.save()
		
		
	i = 0;
	
	for cell in j['cells']:
						
		if cell["type"] in ["basic.twoTextRect","basic.youtubeVideo"]:
			if cell['attrs']['.']['display'] == 'none':
				display = False
			else:
				display = True
				i = i+1
			
			elem, created = Elemgraph.objects.update_or_create(
					graph=graph, 
					proposition = Proposition.objects.get(id = cell['id_prop']), 
					defaults={
						'x': cell['position']['x'],
						'y': cell['position']['y'],
						'displayed':display
						})
	
	graph.propNumber = i
	graph.save()
						
	return HttpResponse('ok')
	
def new_graph(request):
		
	graph = Graph(
		autor = request.user,
		title = request.POST['graphTitle'],
		creation_date = datetime.now()
		)
	graph.save()
	
	return HttpResponseRedirect(reverse('final_viewer', args=(graph.pk,)))

def ajax_newsyllogism(request):
	
	syl = Proposition(
		autor = request.user,
		text = '&',
		nature = 'SY',
		cycle = Cycle.objects.get(pk=1),	
		creation_date = datetime.now(),
		modification_date = datetime.now(),	
	)
	
	syl.save();
	
	majorLink = Link(
		autor = request.user,
		creation_date = datetime.now(),
		modification_date = datetime.now(),
		nature = 'Syl',
		type = LinkType.objects.get(type = 'syllogisme'),
		cycle = Cycle.objects.get(pk=1),
		left_prop = Proposition.objects.get(pk=request.POST['majorPremise']),
		right_prop = syl		
	)
	
	majorLink.save()
	
	minorLink = Link(
		autor = request.user,
		creation_date = datetime.now(),
		modification_date = datetime.now(),
		nature = 'Syl',
		type = LinkType.objects.get(type = 'syllogisme'),
		cycle = Cycle.objects.get(pk=1),
		left_prop = Proposition.objects.get(pk= request.POST['minorPremise']),
		right_prop = syl
	)
	
	minorLink.save()
	
	conclusionLink = Link(
		autor = request.user,
		creation_date = datetime.now(),
		modification_date = datetime.now(),
		nature = 'Syl',
		type = LinkType.objects.get(type = 'donc'),
		cycle = Cycle.objects.get(pk=1),
		left_prop = syl,
		right_prop = Proposition.objects.get(pk=request.POST['syllogismConclusion'])
	)
	
	conclusionLink.save()
	
	all_items = list([syl]) + list([majorLink]) + list([minorLink]) + list([conclusionLink])
	return JsonResponse(serializers.serialize('json', all_items), safe = False)	

def ajax_addexistingprop(request):
	
	main_prop = Proposition.objects.get(pk = request.POST['id'])
	
def	ajax_addcommentgraph(request):

	prop = None
	link = None
	text = request.POST['text']
	
	list_arobase = [word for word in text.split() if word.startswith('@')]
	if len(list_arobase) > 0:
		id_prop = int(list_arobase[0].replace('@',''))
		text = text.replace(list_arobase[0],'')	
		prop = Proposition.objects.get(pk=id_prop)
		
	list_hash = [word for word in text.split() if word.startswith('#')]
	if len(list_hash) > 0:
		id_link = int(list_hash[0].replace('#',''))
		text = text.replace(list_hash[0],'')	
		link = Link.objects.get(pk=id_link)		
		
	comment = CommentGraph(
		graph = Graph.objects.get(pk = request.POST['graph_id']),
		author = request.user,
		text = text,
		creation_date = datetime.now(),
		proposition = prop,
		link = link
	)
	comment.save()
	return JsonResponse(serializers.serialize('json', [comment]), safe = False)
	
def ajax_hidecomment(request):
	
	comment = CommentGraph.objects.get(pk = request.POST['comment'])
	comment.visibility = False
	comment.save()
	
	return HttpResponse('ok')
	
def init(request):

	json_linktypes = [	
		{ 
			'type': 'donc' ,
			'text': '... donc ...',
			'logic': '... donc ...',
			'sens': False,
			'inverse': 'car',
			'strokeColor': '#2EC4B6',
			'strokeWidth': 4,
			'arrows': 1
		},
		{ 
			'type': 'car',
			'text': '... car ...',
			'logic': '... car ...',
			'sens': True,
			'inverse': 'donc',
			'strokeColor': '#2EC4B6',
			'strokeWidth': 4,
			'arrows': 1
		},		
		{ 
			'type': 'concurrence',
			'text': 'Concurrence / Désaccord :',
			'logic': '... est incompatible avec ...',
			'sens': False,
			'inverse': 'concurrence',
			'strokeColor': '#E71D36',
			'strokeWidth': 4,
			'arrows': 2
		},
		{ 
			'type': 'exemple',
			'text': 'Exemple :',
			'logic': '... est illustré par ...',
			'sens': False,
			'inverse': 'théorie',
			'strokeColor': '#2EC4B6',
			'strokeWidth': 4,
			'arrows': 1
		},
		{ 
			'type': 'théorie',
			'text': 'Théorisation :',
			'logic': '... illustre que ...',
			'sens': True,
			'inverse': 'exemple',
			'strokeColor': '#2EC4B6',
			'strokeWidth': 4,
			'arrows': 1
		},
		{ 
			'type': 'contre-exemple',
			'text': 'Contre-exemple :',
			'logic': '... est invalidé par le fait que ..',
			'sens': False,
			'inverse': 'contre-théorie',
			'strokeColor': '#96281B',
			'strokeWidth': 4,
			'arrows': 1
		},
		{ 
			'type': 'contre-théorie',
			'text': 'Contre-Théorisation :',
			'logic': '... est un élément qui rend impossible que ...',
			'sens': True,
			'inverse': 'contre-exemple',
			'strokeColor': '#96281B',
			'strokeWidth': 4,
			'arrows': 1
		},
		{ 
			'type': 'complément',
			'text': 'Complément :',
			'logic': "... traite du même sujet, et n'est pas incompatible avec ...",
			'sens': False,
			'inverse': 'complément',
			'strokeColor': '#4ECDC4',
			'strokeWidth': 4,
			'arrows': 2
		},	
		{ 
			'type': 'syllogisme',
			'text': 'syllogisme',
			'logic': 'syllogisme' ,
			'sens': False,
			'inverse': 'syllogisme',
			'strokeColor': '#2EC4B6',
			'strokeWidth': 4,
			'arrows': 0
		}	
	]

	for link_type in json_linktypes:
	
		linktype, created = LinkType.objects.update_or_create(
				type = link_type['type'], 
				defaults={
					'type': link_type['type'],
					'text': link_type['text'],
					'logic': link_type['logic'],
					'sens': link_type['sens'],
					'inverse': link_type['inverse'],
					'strokeColor': link_type['strokeColor'],
					'strokeWidth':  link_type['strokeWidth'],
					'arrows': link_type['arrows']				
				})
	
		# link_type = LinkType(
		
			# type = link_type['type'],
			# text = link_type['text'],
			# logic = link_type['logic'],
			# sens = link_type['sens'],
			# inverse = link_type['inverse'],
			# strokeColor = link_type['strokeColor'],
			# strokeWidth =  link_type['strokeWidth'],
			# arrows = link_type['arrows']		
		# )
		
		# link_type.save();
	
	links = Link.objects.all()
	
	for link in links:
		if link.nature == 'Donc':
			link.type = LinkType.objects.get(type = 'donc')
		if link.nature == 'Exemple':
			link.type = LinkType.objects.get(type = 'exemple')
		if link.nature == 'Concurrence':
				link.type = LinkType.objects.get(type = 'concurrence')
		if link.nature == 'Syl':
				link.type = LinkType.objects.get(type = 'syllogisme')
		if link.nature == 'E':
				link.type = LinkType.objects.get(type = 'exemple')
		if link.nature == 'D':
				link.type = LinkType.objects.get(type = 'donc')	
		if link.nature == 'C':
				link.type = LinkType.objects.get(type = 'concurrence')				
			
		link.save();
	
	return HttpResponse('Init OK')