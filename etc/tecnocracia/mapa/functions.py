def prepopulate_map():
    from django.contrib.auth.models import User
    from mapa.models import Terreno
    from tecnocracia import settings
    
    #dummy = User.objects.all()[0]

    for i in range(0, settings.MAPS_MAX_X+1):
        for j in range(0, settings.MAPS_MAX_X+1):
            try:
                Terreno(coord_x=i, coord_y=j).save()
            except:
                pass
            try:
                Terreno(coord_x=i, coord_y=-j).save()
            except:
                pass
            try:
                Terreno(coord_x=-i, coord_y=j).save()
            except:
                pass
            try:
                Terreno(coord_x=-i, coord_y=-j).save()
            except:
                pass


def get_coord():
    from mapa.models import Terreno
    
    
    return True


'''
    Funcao que retorna uma area do mapa com diversos terrenos em torno do ponto (x, y) com raio "radius".
'''
def get_area(x, y, radius):
    from mapa.models import Terreno
    from tecnocracia import settings
    
    #converte os valores para garantir que sao inteiros
    x = int( x )
    y = int( y )
    radius = int( radius )
    
    
    saida = []

    #caso a coordenada y extrapole o minimo permitido
    #sera preciso realizar uma correcao
    extra_min_y = y-radius-settings.MAPS_MIN_Y
    if extra_min_y >= 0:

        extra_min_y = 0
        extra_min_y_range = []
    else:
        extra_min_y_range = range( (settings.MAPS_MAX_Y+extra_min_y+1), (settings.MAPS_MAX_Y+1) )


    #caso a coordenada y extrapole o maximo permitido
    #sera preciso realizar uma correcao
    extra_max_y = settings.MAPS_MAX_Y-(y+radius)
    #raise Exception( extra_max_y )
    if extra_max_y >= 0:

        extra_max_y = 0
        extra_max_y_range = []
    else:
        extra_max_y_range = range( (settings.MAPS_MIN_Y), (settings.MAPS_MIN_Y-extra_max_y) )
    #raise Exception( extra_max_y_range )

    
    #raise Exception( extra_min_y_range )
    if len(extra_min_y_range) > 0:
        extra_min_y_range.extend( range( (y-radius-extra_min_y), (y+radius+1) ) )
        y_range = extra_min_y_range
    elif len(extra_max_y_range) > 0:
        temp = range( (y-radius), (y+radius+1+extra_max_y) )
        temp.extend( extra_max_y_range )
        y_range = temp
    else:
        y_range = range( (y-radius), (y+radius+1) )
        
        
    
    
    for j in y_range:
        pack = Terreno.objects.filter( coord_y=j ).select_related()
        if pack.count() == 0:
            raise Exception('argh!')
        pack = pack.filter(coord_x__lte=(x+radius), coord_x__gte=(x-radius) ).order_by('coord_x')
        saida.append( pack )
    
    return saida