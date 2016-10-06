from django.contrib import admin

from .models import Organisation, Speaker, Event, Record, Photo, Sentence, Question, Converter

class OrganisationAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name')
	
class SpeakerAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','description')

class EventAdmin(admin.ModelAdmin):
	list_display= ('id','organisation','name','date','place','status')
	
class RecordAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','event','speaker')
	
class PhotoAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','event')
	
class SentenceAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id', 'text', 'speaker','order','status')
    
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id','text')
	
class ConverterAdmin(admin.ModelAdmin):
    list_display = ('id','html','event')
	
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Record, RecordAdmin)	
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Converter, ConverterAdmin)