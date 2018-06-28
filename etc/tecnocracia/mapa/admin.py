from django.contrib import admin
from mapa.models import *

'''
class BonusTerrenoInline(admin.StackedInline):
    list_display = ['tipo', 'valor', ]
    search_fields = ['tipo', 'valor', ]
    ordering = ['tipo', 'valor', ]
    
    model = BonusTerreno
    extra = 0


class BonusTerrenoAdmin(admin.ModelAdmin):
    pass

class TipoTerrenoAdmin(admin.ModelAdmin):
    pass



class BonusTerrenoInline(admin.StackedInline):
    model = BonusTerreno

class TipoTerrenoInline(admin.StackedInline):
    model = TipoTerreno
'''

class PecaConstrucaoAdmin(admin.ModelAdmin):
    '''list_display = ['coord_x', 'coord_y']
    search_fields = ['tipo',]
    ordering = ['tipo',]
    
    inlines = [TipoTerrenoInline, ]'''
    extra = 0


class ConstrucaoAdmin(admin.ModelAdmin):
    '''list_display = ['coord_x', 'coord_y']
    search_fields = ['tipo',]
    ordering = ['tipo',]
    
    inlines = [TipoTerrenoInline, ]'''
    extra = 0


class TerrenoAdmin(admin.ModelAdmin):
    list_display = ['coord_x', 'coord_y']
    '''search_fields = ['tipo',]
    ordering = ['tipo',]'''
    
    '''inlines = [ConstrucaoInline, ]'''
    extra = 0


admin.site.register(PecaConstrucao, PecaConstrucaoAdmin)
admin.site.register(Construcao, ConstrucaoAdmin)
admin.site.register(Terreno, TerrenoAdmin)
'''
admin.site.register(TipoTerreno, TipoTerrenoAdmin)
admin.site.register(BonusTerreno, BonusTerrenoAdmin)
'''