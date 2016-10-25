import csv

from django.core import serializers
from django.shortcuts import render

from gdpcore.models import *
from .models import Event, Record, Photo, Sentence, Question, Converter, Speaker, Photo
from django.contrib.auth.models import User
from django.http import HttpResponse
from datetime import datetime 
from django.conf import settings
import os
import json

from django.contrib.auth.decorators import login_required
from collections import Counter
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def index(request):
    events = Event.objects.all().order_by('date')
    return render(request, 'univok/eventsViewer.html', {'events': events});  

def eventViewer(request, id_event):
    event = Event.objects.get(id=id_event)
    photos = Photo.objects.filter(event=event)

    return render(request, 'univok/pastEventViewer.html', {
                    'event': event,
                    'photos': photos
                    })


def animViewer(request, id_event):
    event = Event.objects.get(id=id_event)
    show = event.show
    photos = Photo.objects.filter(event=event)
    showparts = ShowPart.objects.filter(show=show).order_by('order')

    props = []
    links = []
    showlength = 0
    sentences = Sentence.objects.filter(event = event)
    
    for showpart in showparts:
        showpart.proposition.timediff = showpart.proposition.videoEnd - showpart.proposition.videoBeginning
        props.append(showpart.proposition)
        showlength = showlength + showpart.duration

        showpart.proposition.sentences = Sentence.objects.filter(proposition = showpart.proposition)
#        showpart.proposition.authorPicture = Speaker.objects.filter()

    for prop in props:
        rightLinks = Link.objects.filter(right_prop=prop)
        leftLinks = Link.objects.filter(left_prop=prop)

        for rightLink in rightLinks:
            if rightLink.left_prop in props:
                links.append(rightLink)

        for leftLink in leftLinks:
            if leftLink.right_prop in props:
                links.append(leftLink)

    links = list(set(links))
    link_types = LinkType.objects.all()
    
    minutes = int(float(showlength) // 60)
    seconds = int(showlength - minutes*60)
    show.seconds = seconds
    show.minutes = minutes
 #   show.showlength.minutes = minutes
    
    return render(request, 'univok/animViewer.html', {'event': event,
                                                           'photos': photos,
                                                           'show': show,
                                                           'showparts': showparts,
                                                           'link_types': link_types,
                                                           'links': links})    
                                                                
@login_required
def ideasViewer(request, id_event):
    event = Event.objects.get(id=id_event)
    records = Record.objects.filter(event=event)
    sentences = Sentence.objects.filter(event=event)

    graph = event.graph
    comments_graph = CommentGraph.objects.filter(graph=graph)

    elems = Elemgraph.objects.filter(graph=graph)

    props = []
    links = []
    implications = []
    attributes = {}
    for elem in elems:
        if elem.displayed == True:
            attributes[elem.proposition.id] = {'x': elem.x, 'y': elem.y}

            props.append(elem.proposition)

            links_right = Link.objects.filter(left_prop=elem.proposition)
            links_left = Link.objects.filter(right_prop=elem.proposition)

            for link_right in links_right:
                links.append(link_right)
                props.append(link_right.right_prop)

                imps = Implication.objects.filter(link=link_right)
                for imp in imps:
                    implications.append(imp)
                    props.append(imp.proposition)

            for link_left in links_left:
                links.append(link_left)
                props.append(link_left.left_prop)

                imps = Implication.objects.filter(link=link_left)
                for imp in imps:
                    implications.append(imp)
                    props.append(imp.proposition)

            props = list(set(props))
            links = list(set(links))

    link_types = LinkType.objects.all()
    json_linktypes = serializers.serialize('json', link_types)

    return render(request, 'univok/ideasViewer.html', {
        'event': event,
        'records': records,
        'sentences': sentences,
        'graph': graph,
        'link_types': link_types,
        'json_linktypes': json_linktypes,
        'props': props,
        'attributes': attributes,
        'links': links,
        'implications': implications,
        'comments_graph': comments_graph})

@login_required
def sentencesConverter(request, id_event):
    # csvfile = request.FILES['csv']
    # op = open(/static/gdpcore/csvtobedealtwith/aaa.csv,'rb')
    
    event = Event.objects.get(pk = id_event)
    
    if request.method == 'POST':
        converter = Converter(
            html = request.POST['html'],
            event = Event.objects.get(pk = request.POST['event'])       
        )
        
        converter.save()
        return HttpResponse(converter.pk)
    
    text = open(os.path.join(settings.MEDIA_ROOT, 'aaa.csv'), 'r')
    cr = csv.reader(text, delimiter=';')
    sentences = [];
    names = [];
    for row in cr:
        sentences.append(row)
        names.append(row[0])
    names = set(list(names))
    
    converter = Converter.objects.filter(event = event).order_by('-pk')
    
    link_types = LinkType.objects.all()  
    # with open('aaa.csv') as f:
    # reader = csv.reader(f)
    # for row in reader:
    # sentences.append(row)

    return render(request, 'univok/sentencesConverter.html', {
                    'sentences': sentences,
                    'converter':converter,
                    'names': names,
                    'event': event,
                    'link_types':link_types});  

# else:
# return render(request,'univok/csvUploader.html',{'aaa': 0 });

@login_required
def collectif(request):
    return render(request, 'univok/collectif.html')

def ajax_newquestion(request):
    
    question = Question(
        text = request.POST['text'],
        firstname = request.POST['name'],
        lastname = request.POST['name'],
        email = request.POST['email'],
        phone = request.POST['phone'],
        time = datetime.now(),
        event = Event.objects.get(pk = request.POST['event'])
    )    
    question.save()
    
    showparts = request.POST.getlist('showpartIds[]')
    for showpart in showparts:
        question.showpart.add(ShowPart.objects.get(pk=showpart))
 
 
    fromaddr = "polikif@gmail.com"
    toaddr = "gouriten.arthur@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Nouvelle question de "+ request.POST['name']
     
    body = "Nouvelle question de "+ request.POST['name']+". Plus d'infos: ecossolies.univok.fr/deepview/"+request.POST['event']
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "tabouret")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit() 
    
    return HttpResponse(question.pk)

@login_required    
def finalBuilder(request):

    sentencesTable = json.loads(request.POST['sentencesTable'])
    propsTable = json.loads(request.POST['propsTable'])
    linksTable = json.loads(request.POST['linksTable'])
    
    props = {}
    corresp = {}
    order = 0
    orderShow = 1
    
    finalAuthor, created = User.objects.get_or_create(
        username='Univok',
        password='Univok'
    )    
    
    show = Event.objects.get(pk = request.POST['event']).show

    for propRow in propsTable['myrows']:
        if len(propRow) > 0:
            if len(propRow['propText']) > 0:
            

            
                prop = Proposition(          
                    autor = finalAuthor,
                    text = propRow['propText'],
                    creation_date = datetime.now(),
                    modification_date = datetime.now(),               
                )
                
                prop.save()
                props[propRow['propId']] = prop
                
 
                showpart = ShowPart(
                    show = show,
                    order = orderShow,
                    proposition = prop,
                    x = propRow['propX'],
                    y = propRow['propY'],
                    duration = 2
                )
                showpart.save()
                orderShow = orderShow+1

    for linkRow in linksTable['myrows']:
        if len(linkRow) > 0:
            if len(linkRow['leftId']) > 0:              
                link = Link(              
                    autor = finalAuthor,
                    creation_date = datetime.now(),
                    modification_date = datetime.now(),
                    type = linkRow['linkType'],                         
                    left_prop = props[ linkRow['leftId'] ],
                    right_prop = props[linkRow['rightId']]                 
                )
                
                link.save()
                
        
    for sentenceRow in sentencesTable['myrows']:
    
        if len(sentenceRow) > 0:
            if len(sentenceRow['sentenceIni']) > 0:
        
                obj, created = Speaker.objects.get_or_create(
                    name = sentenceRow['author'],
                    defaults={'description':'default', 'picture':'default'},
                )
        
                sentence = Sentence(
                    event = Event.objects.get(pk = request.POST['event']),
                    speaker = obj,
                    order = order,
                    text = sentenceRow['sentenceIni'],
                    status = int(sentenceRow['status'])
                )
            
                sentence.save()
                
                propids = sentenceRow['sentenceProp']
                
                if len(propids) > 0:
                
                    listids = propids.split(',')
                    
                    for id in listids:
                        sentence.proposition.add(props[id])               
                    order = order+1
                
     
    # for prop in props:
        # sentences = prop.sentence_set.all().order_by('order')
        # if len(sentences)>0:
            # author, created = User.objects.get_or_create(
                # username=sentences[0].speaker.name,
                # password=sentences[0].speaker.name
            # )
            
            # prop.autor = author
            # prop.save()        
     
         
     
                
    return HttpResponse('OKAYYYYYYYYYYYY')
    
  
def deepview(request, id_event):
    
    event = Event.objects.get(pk = id_event)
    
    photos = Photo.objects.filter(event = event)
    records = Record.objects.filter(event = event)
    questions = Question.objects.all().order_by('-time')
    sentences = Sentence.objects.filter(event = event)
    
    
    count={}
    count['total'] = 0
    
    longString = ''
    
    for sentence in sentences:
        longString = longString +' '+ sentence.text
    
        if sentence.speaker.name in count:
            count[sentence.speaker.name] = count[sentence.speaker.name] + len(sentence.text)
        else:
            count[sentence.speaker.name] = len(sentence.text)
        count['total'] = count['total'] + len(sentence.text)
    
    d = sorted(count, key=count.get)
    
    final_count = []
    for author in d:
        final_count.append({author: count[author]})

    
    wordList = re.sub("[^\w]", " ",  longString).split()
    wordCount = Counter(wordList)    

    return render(request, 'univok/deepview.html', {'event': event, 
                                    'photos':photos, 
                                    'records':records,
                                    'questions':questions,
                                    'final_count': final_count, 
                                    'wordCount': wordCount});

@login_required
def simpleGraphViewer(request, id_show):
    show = Show.objects.get(pk = id_show)
    showparts = ShowPart.objects.filter(show = show)
    
    props = []
    links = []

    
    for showpart in showparts:
        showpart.proposition.timediff = showpart.proposition.videoEnd - showpart.proposition.videoBeginning
        props.append(showpart.proposition)

        showpart.proposition.sentences = Sentence.objects.filter(proposition = showpart.proposition)
#        showpart.proposition.authorPicture = Speaker.objects.filter()

    for prop in props:
        rightLinks = Link.objects.filter(right_prop=prop)
        leftLinks = Link.objects.filter(left_prop=prop)

        for rightLink in rightLinks:
            if rightLink.left_prop in props:
                links.append(rightLink)

        for leftLink in leftLinks:
            if leftLink.right_prop in props:
                links.append(leftLink)

    links = list(set(links))
       
    return render(request, 'univok/simpleGraphViewer.html', {'show': show,
                                                           'showparts': showparts,
                                                           'props': props,
                                                           'links': links})    

@login_required                                                           
def propsAuthorGenerator(request):
    props = Proposition.objects.all()
    for prop in props:
        sentences = prop.sentence_set.all().order_by('order')
        if len(sentences)>0:
            author, created = User.objects.get_or_create(
                username=sentences[0].speaker.name,
                password=sentences[0].speaker.name
            )
            
            prop.autor = author
            prop.save() 
            
    return HttpResponse('OKAAAAAAAAY')
        
def reviewAsList(request, id_event):
    event = Event.objects.get(id=id_event)
    show = event.show
    photos = Photo.objects.filter(event=event)
    showparts = ShowPart.objects.filter(show=show).order_by('themeOrder')

    props = []
    links = []
    showlength = 0
    sentences = Sentence.objects.filter(event = event)
    
    for showpart in showparts:
        showpart.proposition.timediff = showpart.proposition.videoEnd - showpart.proposition.videoBeginning
        props.append(showpart.proposition)
        showlength = showlength + showpart.duration

        showpart.proposition.sentences = Sentence.objects.filter(proposition = showpart.proposition)
#        showpart.proposition.authorPicture = Speaker.objects.filter()

    for prop in props:
        rightLinks = Link.objects.filter(right_prop=prop)
        leftLinks = Link.objects.filter(left_prop=prop)

        for rightLink in rightLinks:
            if rightLink.left_prop in props:
                links.append(rightLink)

        for leftLink in leftLinks:
            if leftLink.right_prop in props:
                links.append(leftLink)

    links = list(set(links))
    
    minutes = int(float(showlength) // 60)
    seconds = int(showlength - minutes*60)
    show.seconds = seconds
    show.minutes = minutes
 #   show.showlength.minutes = minutes
 
    themes = ShowPart.objects.filter(show=show).order_by('theme').values('theme').distinct()
    names = ShowPart.objects.filter(show=show).order_by('proposition__autor__username').values('proposition__autor__username').distinct()
    
    return render(request, 'univok/reviewAsList.html', {'event': event,
                                                           'photos': photos,
                                                           'show': show,
                                                           'showparts': showparts,
                                                           'links': links,
                                                           'sentences':sentences,
                                                           'themes': themes,
                                                           'names':names})   

def reviewSimple(request, id_show):
    show = Show.objects.get(pk = id_show)
    showparts = ShowPart.objects.filter(show=show).filter(synthese = 0).order_by('themeOrder')

    props = []
    links = []
    showlength = 0
    
    for showpart in showparts:
        showpart.proposition.timediff = showpart.proposition.videoEnd - showpart.proposition.videoBeginning
        props.append(showpart.proposition)
        showlength = showlength + showpart.duration

        showpart.proposition.sentences = Sentence.objects.filter(proposition = showpart.proposition)

    for prop in props:
        rightLinks = Link.objects.filter(right_prop=prop)
        leftLinks = Link.objects.filter(left_prop=prop)

        for rightLink in rightLinks:
            if rightLink.left_prop in props:
                links.append(rightLink)

        for leftLink in leftLinks:
            if leftLink.right_prop in props:
                links.append(leftLink)

    links = list(set(links))
    
    minutes = int(float(showlength) // 60)
    seconds = int(showlength - minutes*60)
    show.seconds = seconds
    show.minutes = minutes
 #   show.showlength.minutes = minutes
 
    themes = ShowPart.objects.filter(show=show).order_by('theme').values('theme').distinct()
    names = ShowPart.objects.filter(show=show).order_by('proposition__autor__username').values('proposition__autor__username').distinct()
    
    return render(request, 'univok/reviewSimple.html', {   'show': show,
                                                           'showparts': showparts,
                                                           'links': links,
                                                           'themes': themes,
                                                           'names':names})  
                                                           
@login_required                                                           
def reviewAsListBuilder(request, id_event):
    
    if request.method == 'POST':
        propsTable = json.loads(request.POST['propsTable'])
        for propRow in propsTable['myrows']:
            if (len(propRow) > 0):
                showpart = ShowPart.objects.get(pk= propRow['showpartId'])
                showpart.theme = propRow['theme']
                showpart.themeOrder = propRow['themeOrder']
                showpart.themePrefix = propRow['themePrefix']            
                showpart.save()       
        
        return HttpResponse('OK');
    
    event = Event.objects.get(id=id_event)
    show = event.show
    photos = Photo.objects.filter(event=event)
    showparts = ShowPart.objects.filter(show=show).order_by('themeOrder')

    props = []
    links = []
    showlength = 0
    sentences = Sentence.objects.filter(event = event)
    
    for showpart in showparts:
        showpart.proposition.timediff = showpart.proposition.videoEnd - showpart.proposition.videoBeginning
        props.append(showpart.proposition)
        showlength = showlength + showpart.duration

        showpart.proposition.sentences = Sentence.objects.filter(proposition = showpart.proposition)
#        showpart.proposition.authorPicture = Speaker.objects.filter()

    for prop in props:
        rightLinks = Link.objects.filter(right_prop=prop)
        leftLinks = Link.objects.filter(left_prop=prop)

        for rightLink in rightLinks:
            if rightLink.left_prop in props:
                links.append(rightLink)

        for leftLink in leftLinks:
            if leftLink.right_prop in props:
                links.append(leftLink)

    links = list(set(links))
    
    minutes = int(float(showlength) // 60)
    seconds = int(showlength - minutes*60)
    show.seconds = seconds
    show.minutes = minutes
 #   show.showlength.minutes = minutes
    themes = ShowPart.objects.filter(show=show).order_by('theme').values('theme').distinct()
    
    return render(request, 'univok/reviewAsListBuilder.html', {'event': event,
                                                           'photos': photos,
                                                           'show': show,
                                                           'showparts': showparts,
                                                           'links': links,
                                                           'sentences':sentences,
                                                           'themes': themes})  

@login_required 
def duplicateShow(request, id_show):

    show = Show.objects.get(pk = id_show)
    newshow = Show(
        author = show.author,
        title = show.title,
        description = show.description,
        audio = show.audio    
    )  
    newshow.save()
    
    showparts = ShowPart.objects.filter(show = show)
    for showpart in showparts:
        newshowpart = ShowPart(
            show = newshow,
            order = showpart.order,
            text = showpart.text,
            proposition = showpart.proposition,
            x = showpart.x,
            y = showpart.y,
            link = showpart.link,
            duration = showpart.duration,
            audio = showpart.audio,
            
            theme = showpart.theme,
            themeOrder = showpart.themeOrder,
            themePrefix = showpart.themePrefix      
        )
        newshowpart.save()
        
    return HttpResponse(newshow.pk)