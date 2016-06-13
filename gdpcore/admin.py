from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Cycle, Proposition, LinkType, Link, Comment, Notification, Implication, Graph, Elemgraph, UserProfile, CommentGraph

class CycleAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','text','autor')
	
class PropositionAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','text','autor')

class LinkTypeAdmin(admin.ModelAdmin):
	list_display= ('id','type','sens','text','inverse','logic','strokeColor','arrows')
	
class LinkAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','nature','type', 'autor')
	
class CommentAdmin(admin.ModelAdmin):
	list_display = ('id','text', 'autor','proposition')
	
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('id','nature', 'autor')	
	
class ImplicationAdmin(admin.ModelAdmin):
	list_display = ('id','autor')	
	
class GraphAdmin(admin.ModelAdmin):
	list_display = ('id', 'autor', 'graphstring', 'title')	

class ElemgraphAdmin(admin.ModelAdmin):
	list_display = ('id', 'x', 'y', 'graph', 'proposition','displayed')	
	
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'picture')
	
class CommentGraphAdmin(admin.ModelAdmin):
	list_display = ('id', 'graph', 'text', 'author')
	
admin.site.register(Cycle, CycleAdmin)
admin.site.register(Proposition, PropositionAdmin)
admin.site.register(LinkType, LinkTypeAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Implication, ImplicationAdmin)
#admin.site.register(Graph, GraphAdmin)
admin.site.register(Elemgraph, ElemgraphAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CommentGraph, CommentGraphAdmin)

admin.site.register(Graph, SimpleHistoryAdmin)