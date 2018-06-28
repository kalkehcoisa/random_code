

class AliasConflict(Exception):
    '''
    Exceção para o caso de tentar cadastrar um comando com um alias
    que já existe.
    '''
    def __init__(self, alias, *ag, **kw):
        self.msg = 'Já há um comando registrado com o alias "{alias}"!'.format(
            alias=alias)
        super(self.__class__, self).__init__(self.msg, *ag, **kw)


class AliasUnregistered(Exception):
    '''
    Exceção para o caso de tentar executar um comando com um alias
    não registrado.
    '''
    def __init__(self, alias, *ag, **kw):
        self.msg = 'Não há um comando registrado com o alias "{alias}"!'
        self.msg = self.msg.format(alias=alias)
        super(self.__class__, self).__init__(self.msg, *ag, **kw)


class ColorValue(Exception):
    '''
    Classe lançada pelo método create quando um dos
    parâmetros é <= 0.
    '''
    def __init__(self, *ag, **kw):
        self.msg = 'Ambas medidas da matriz devem ser maiores que 0.'
        super(self.__class__, self).__init__(self.msg, *ag, **kw)


class ColorLength(Exception):
    '''
    Classe lançada pelo método create quando um dos
    parâmetros é <= 0.
    '''
    def __init__(self, *ag, **kw):
        self.msg = 'Ambas medidas da matriz devem ser maiores que 0.'
        super(self.__class__, self).__init__(self.msg, *ag, **kw)


class InvalidSize(Exception):
    '''
    Classe lançada pelo método create quando um dos
    parâmetros é <= 0.
    '''
    def __init__(self, *ag, **kw):
        self.msg = 'Ambas medidas da matriz devem ser maiores que 0.'
        super(self.__class__, self).__init__(self.msg, *ag, **kw)
