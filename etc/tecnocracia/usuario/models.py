# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from django.contrib.auth.models import User

from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MaxLengthValidator

from thumbs import ImageWithThumbsField

from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey 


CHOICES_KIND_USER = (
                        ('joga', 'Jogador'),
                        ('natu', 'Natureza'),
                        ('mons', 'Monstros'),
                        ('nati', 'Nativos'),
                    )

CHOICES_EDICAO_YEAR = ( (str(p), str(p)) for p in range(1990, datetime.now().year+1) )
CHOICES_EDICAO_MONTH = ( (str(p), _(datetime(1901, p, 1).strftime("%B")) ) for p in range(1, 13) )



class UserProfile(models.Model):
    tipo = models.CharField(max_length=20, null=False, blank=False, choices=CHOICES_KIND_USER)
    agressivo = models.NullBooleanField(default=0)
    ataca_proximidades = models.BooleanField(default=0)
    
    phone = models.CharField(max_length=20, null=False, blank=True, verbose_name=_("Telefone"), default='' )
    code = models.CharField(max_length=4, null=False, blank=True, verbose_name=_("Area code"), default='' )
    user = models.OneToOneField(User, null=False, blank=False)
    
    #operating_sectors = models.ForeignKey( Sector, null=True, unique=False, verbose_name=_("Setor da economia") )
    #operating_subsectors = ChainedForeignKey( SubSector, chained_field='operating_sectors', chained_model_field='sector', null=True, unique=False, verbose_name=_("Area de atuacao") )
    
class Jogador(models.Model):
    pass