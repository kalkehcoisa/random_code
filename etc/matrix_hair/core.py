#!/usr/bin/python3

import exceptions


class Commandhandler:
    '''
    Classe para encapsular, gerenciar e associar
    valores úteis para o trabalho com os comandos.

    * `_alias`: armazena um novo nome ao comando
    * `_command`: o próprio comando

    * `_commands`: atributo de classe que armazena os comandos
    registrados. Usada para chamá-los e garantir unicidade de aliases.
    '''

    _commands = dict()

    def __init__(self, command, alias):
        self.__class__._register_new(command, alias)

    def __call__(self, *ag, **kw):
        '''
        Executa o comando armazenado neste objeto.
        '''
        return self._command(*ag, **kw)

    @classmethod
    def _register_new(cls, command, alias):
        '''
        Registra o comando na lista global de comandos da classe.
        Se o alias já estiver registrado, lança uma exceção.
        '''

        if alias not in cls._commands.keys():
            cls._commands[alias] = command
        else:
            raise exceptions.AliasConflict(alias)

    @classmethod
    def command(cls, alias):
        '''
        Decorator montado usando a classe Commandhandler para
        encapsular os comandos e associar valores úteis para
        o trabalho com eles.
        '''
        def decorator(func):
            return Commandhandler(func, alias)
        return decorator

    @classmethod
    def run(cls, alias, *ag, **kw):
        '''
        Executa o comando associado ao alias informado.
        Ou lança exceção se o comando não estiver registrado.
        '''
        if alias in cls._commands.keys():
            cls._commands[alias](*ag, **kw)
        else:
            raise exceptions.AliasUnregistered(alias)


class InputHandler:
    '''
    Recebe, trata e direciona as requisições do usuário.
    '''
    def __init__(self, valid_commands):
        '''
        Recebe um iterável com os nomes dos comandos aceitos.
        '''
        self._valid_commands = set(valid_commands)

    def read(self, command):
        if command not in self._valid_commands:
            raise Exception('Aqui')


class Shell:
    '''
    Interface final para comunicação com o usuário.
    '''

    _input_h = None
    _command_handler = None

    def __init__(self, input_handler, command_handler):
        '''
        Requer os objetos para gerenciar entrada e comandos.
        '''
        self._input_handler = input_handler
        self._command_handler = command_handler
