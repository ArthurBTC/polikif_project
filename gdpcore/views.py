from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Proposition, Link, Cycle, Comment, Notification, Implication
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from difflib import SequenceMatcher

from datetime import datetime  

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