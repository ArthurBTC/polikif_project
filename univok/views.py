from django.shortcuts import render
from .models import Organisation, Speaker, Event, Record, Photo, Sentence
from gdpcore.models import *

from django.core import serializers
from io import StringIO
import json
import requests
import csv
from django.contrib.staticfiles.templatetags.staticfiles import static

# Create your views here.
def index(request):
	events = Event.objects.all()
	return render(request,'univok/eventsViewer.html',{'events': events });

	
def eventViewer(request, id_event):
	event = Event.objects.get(id = id_event)
	show = event.show

	showparts = ShowPart.objects.filter(show = show).order_by('order')
	
	props = []
	links = []
	
	for showpart in showparts:
		showpart.proposition.timediff = showpart.proposition.videoEnd -showpart.proposition.videoBeginning
		props.append(showpart.proposition)
	
	for prop in props:
		rightLinks = Link.objects.filter(right_prop = prop)
		leftLinks = Link.objects.filter(left_prop = prop)
		
		for rightLink in rightLinks:
			if rightLink.left_prop in props:
				links.append(rightLink)
		
		for leftLink in leftLinks:
			if leftLink.right_prop in props:
				links.append(leftLink)
				
	links = list(set(links))			
	link_types = LinkType.objects.all()
		

	if event.status == '1':
	
		photos = Photo.objects.filter(event=event)	
		return render(request,'univok/pastEventViewer.html',{'event': event, 
					'photos': photos,
					'show': show,
					'showparts':showparts,
					'link_types':link_types,
					'links':links})

		
	if event.status == '0':
		return render(request,'univok/futurEventViewer.html',{'event': event });
		
def ideasViewer(request, id_event):
	event = Event.objects.get(id = id_event)
	records = Record.objects.filter(event = event)
	sentences = Sentence.objects.filter(event=event)
			 	
	
	graph = event.graph
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

	
	return render(request,'univok/ideasViewer.html',{
					'event': event,
					'records': records,
					'sentences': sentences,
					'graph': graph,
					'link_types': link_types,
					'json_linktypes': json_linktypes,
					'props': props,
					'attributes': attributes, 
					'links':links,
					'implications': implications,
					'comments_graph': comments_graph})

def sentencesConverter(request):
	
	# csvfile = request.FILES['csv']
	# op = open(/static/gdpcore/csvtobedealtwith/aaa.csv,'rb')
	from django.conf import settings
	import os
	text = open(os.path.join(settings.MEDIA_ROOT, 'aaa.csv'), 'r')
	cr = csv.reader(text, delimiter=';')	
	sentences=[];
	names=[];
	for row in cr:
		sentences.append(row)
		names.append(row[0])
	names = set(list(names))	
	# with open('aaa.csv') as f:
		# reader = csv.reader(f)
		# for row in reader:
			# sentences.append(row)
		
	return render(request,'univok/sentencesConverter.html',{'sentences': sentences, 'names':names });
	# else:
		# return render(request,'univok/csvUploader.html',{'aaa': 0 });