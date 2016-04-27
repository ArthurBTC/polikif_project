from django.contrib import admin

from .models import Parti, Cellule, Adhesion_parti, Adhesion_cellule, Selection

class PartiAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name')
	
class CelluleAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','name','parti')

class Adhesion_partiAdmin(admin.ModelAdmin):
    # ...
    list_display = ('id','user', 'parti')
	
class Adhesion_celluleAdmin(admin.ModelAdmin):
	list_display = ('id','user', 'cellule')
	
class SelectionAdmin(admin.ModelAdmin):
	list_display = ('id','parti', 'status')	
	

admin.site.register(Parti, PartiAdmin)
admin.site.register(Cellule, CelluleAdmin)
admin.site.register(Adhesion_parti, Adhesion_partiAdmin)
admin.site.register(Adhesion_cellule, Adhesion_celluleAdmin)
admin.site.register(Selection, SelectionAdmin)
