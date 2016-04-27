from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Parti, Cellule, Adhesion_parti, Selection
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import F
from django.db import models

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from difflib import SequenceMatcher

from datetime import datetime  





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
def parti_accueil(request):
	partis = Parti.objects.all()
	return render(request,'polikif/parti_accueil.html',{'partis':partis})

#Vue d'un parti
def parti_presentation(request, id_parti):

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
		main_parti = Parti.objects.get(id = id_parti)
		cellules = Cellule.objects.filter(parti = main_parti)
		return render(request,'polikif/parti_presentation.html',{'main_parti':main_parti, 'partis':partis, 'cellules':cellules})
	
#Vue d'un programme de parti
def programme_visualisation(request, id_parti):
	
	main_parti = Parti.objects.get(id = id_parti)
	selections = Selection.objects.filter(parti = Parti.objects.get(id= id_parti))
	categories = Selection.objects.filter(parti = Parti.objects.get(id= id_parti)).values("category").annotate(n=models.Count("pk"))
	
	return render(request,'polikif/programme_visualisation.html',{'selections': selections, 'main_parti': main_parti, 'categories':categories})
	
#Vue des membres d'un parti
def membres_parti_visualisation(request, id_parti):
	return render(request,'polikif/index.html')
	
#Vue des cellules, accueil
def cellule_accueil(request):
	return render(request,'polikif/index.html')
	
#Vue d'une cellule
def cellule_presentation(request, id_cellule):
	return render(request,'polikif/index.html')
	
	

	
	
	