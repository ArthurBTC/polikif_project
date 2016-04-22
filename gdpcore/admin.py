from django.contrib import admin

from .models import Cycle, Proposition, Link, Comment, Notification

class CycleAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','text','autor')
	
class PropositionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','text','autor')

class LinkAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','nature', 'autor')
	
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','text', 'autor','proposition')
	
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('id','nature', 'autor')	
	

admin.site.register(Cycle, CycleAdmin)
admin.site.register(Proposition, PropositionAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
