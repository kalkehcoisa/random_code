# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxValueValidator, MinValueValidator

from tecnocracia import settings
from tecnocracia.thumbs import ImageWithThumbsField


TIPOS_DE_RECURSO = (
                        (1, 'Vegetal'),
                        (2, 'Mineral'),
                   )
TIPOS_DE_TERRENO =(
                     (1, 'Gramado'),
                     (2, 'Deserto'),
                     (3, 'Rochas')
                  )

'''
class Recurso(models.Model):
    tipo = models.CharField(max_length=20, choices=TIPOS_DE_BONUS_TERRENO)
    valor = models.IntegerField(default=0)
'''


class Construcao(models.Model):

    nome = models.CharField(max_length=200)
    numero_de_campos = models.IntegerField()
    
    def __unicode__(self):
        aux = ( smart_str(self.nome) ).decode('utf-8')
        return aux


class PecaConstrucao(models.Model):
    nome = models.CharField(max_length=200)
    imagem = ImageWithThumbsField( upload_to='img_construcao', sizes=((50, 50),) )
    
    construcao = models.ForeignKey(Construcao, null=True, blank=True,)
    
    ordenacao = models.PositiveIntegerField(null=True, blank=True)
    
    def __unicode__(self):
        aux = ( smart_str(self.nome) ).decode('utf-8')
        return aux


class Terreno(models.Model):

    coord_x = models.IntegerField(validators = [MaxValueValidator(settings.MAPS_MAX_X), MinValueValidator(settings.MAPS_MIN_X)])
    coord_y = models.IntegerField(validators = [MaxValueValidator(settings.MAPS_MAX_Y), MinValueValidator(settings.MAPS_MIN_Y)])
    
    imagem = ImageWithThumbsField( upload_to='img_terreno', sizes=((50, 50),), default=settings.MEDIA_URL+'img_terreno/grass.png')
    
    peca_construcao = models.ForeignKey(PecaConstrucao, null=True, blank=True, )

    
    def __unicode__(self):
        aux = ( smart_str(self.coord_x)+', '+smart_str(self.coord_y) ).decode('utf-8')
        return aux
    
    
    class Meta:
        unique_together = ('coord_x', 'coord_y',)
        ordering=('coord_x', 'coord_y')

    '''
    class Meta:
        app_label = "Acervo"
        db_table = "acervo_secao"

        verbose_name = ("Se&ccedil;&atilde;o")
        verbose_name_plural = ("Se&ccedil;&otilde;es")
        ordering=('coord_x', 'coord_y')
    '''

    def save(self, *args, **kwargs):
        #settings.MAPS_MAX_Y
        
        
        super(Terreno, self).save(*args, **kwargs) # Call the "real" save() method.
    

