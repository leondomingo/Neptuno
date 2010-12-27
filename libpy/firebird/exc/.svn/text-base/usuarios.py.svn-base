# -*- coding: utf-8 -*-

class EUsuariosBase(Exception):
    def __init__(self):
        Exception.__init__(self)
        
class ENoExisteUsuario(EUsuariosBase):
    def __init__(self, cod_usuario):
        EUsuariosBase.__init__(self)
        self.cod_usuario = cod_usuario
        
    def __str__(self):
        return 'Login incorrecto: %s' % str(self.cod_usuario)
        
class ELoginIncorrecto(EUsuariosBase):
    def __init__(self, login):
        EUsuariosBase.__init__(self)
        self.login = login
        
    def __str__(self):
        return 'Login incorrecto: %s' % str(self.login)