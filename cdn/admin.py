from django.contrib import admin
from .models import Member, Event, Place, Presence

class MemberAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','role','status')
	
class EventAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','status','organisator','time')

class PlaceAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','adress')

class PresenceAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','member','event','guest')

admin.site.register(Member, MemberAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Presence, PresenceAdmin)

