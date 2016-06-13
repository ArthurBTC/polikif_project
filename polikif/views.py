from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Parti, Cellule, Adhesion_parti, Selection
from gdpcore.models import Graph
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import F
from django.db import models

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from difflib import SequenceMatcher

from datetime import datetime, timedelta





# Accueil
def index(request):
	
	member = False
	try:
		adhpar = Adhesion_parti.objects.filter(user=request.user).filter(status = 'A')
		if adhpar.count() != 0:
			member = True
		return render(request,'polikif/index.html',{'member': member})	
	except:
		return render(request,'polikif/index.html',{'member': member})
	
	

#Vue des Partis, accueil
def accueilPartis(request):
	partis = Parti.objects.all()
	return render(request,'polikif/accueilPartis.html',{'partis':partis})

#Vue d'un parti
def partiPresentation(request, id_parti):

	if request.method == 'POST':
		adhpar = Adhesion_parti(user = request.user,
								parti = Parti.objects.get(id=id_parti),
								role = 'M',
								status = 'A',
								creation_date = datetime.now()
								)
		adhpar.save()
		return render(request,'polikif/confirmation_postuler.html',{'adhpar':adhpar})
			
	else :	
		partis = Parti.objects.all()
		parti = Parti.objects.get(id = id_parti)
		cellules = Cellule.objects.filter(parti = parti)
		return render(request,'polikif/partiPresentation.html',{'parti':parti, 'partis':partis, 'cellules':cellules})
	
#Vue d'un programme de parti
def partiProgramme(request, id_parti):
	
	parti = Parti.objects.get(id = id_parti)
	selections = Selection.objects.filter(parti = Parti.objects.get(id= id_parti))
	categories = Selection.objects.filter(parti = Parti.objects.get(id= id_parti)).values("category").annotate(n=models.Count("pk"))
	
	return render(request,'polikif/partiProgramme.html',{'selections': selections, 'parti': parti, 'categories':categories})
	
#Vue des membres d'un parti
def partiMembres(request, id_parti):
	
	parti = Parti.objects.get(id = id_parti)
	adhesions = Adhesion_parti.objects.filter(parti__pk = id_parti)
	
	data = {}
	baba = []
	
	

	for i in range(0, 30):
		dataDate = datetime.now() + timedelta(days = i - 29)
	
		try:		
			baba.append( (dataDate, parti.history.as_of(dataDate).memberCount) )
		except:
			baba.append( (dataDate, 0 ) )

	return render(request,'polikif/partiMembres.html', {'parti': parti, 'adhesions':adhesions, 'baba':baba})	
	
def partiPublications(request, id_parti):
	
	parti = Parti.objects.get(id = id_parti)
	
	return render(request,'polikif/partiPublications.html',{'parti': parti})
		
def partiTravaux(request, id_parti):
	
	parti = Parti.objects.get(id = id_parti)
	graphs = Graph.objects.filter(parti__pk = id_parti)
	
	return render(request,'polikif/partiTravaux.html',{'parti': parti, 'graphs':graphs})		
	
	
def userPresentation(request, id_user):

	selectedUser = User.objects.get(id = id_user)
	
	return render(request,'polikif/userPresentation.html',{'selectedUser': selectedUser})
	
def travauxListe(request):
	
	graphs = Graph.objects.all()

	return render(request,'polikif/travauxListe.html',{'graphs':graphs})
	
#Vue des cellules, accueil
def cellule_accueil(request):
	return render(request,'polikif/index.html')
	
#Vue d'une cellule
def cellule_presentation(request, id_cellule):
	return render(request,'polikif/index.html')
	
	

	
	
	