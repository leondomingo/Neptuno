# -*- coding: utf-8 -*-

class EUsuariosWebBase(Exception):
    def __init__(self):
        Exception.__init__(self)
        
class ENoExisteUsuarioWeb(EUsuariosWebBase):
    def __init__(self, login):
        EUsuariosWebBase.__init__(self)
        self.login = login
        
    def __str__(self):
        return 'No existe el usuario web %s' % self.login
    
class EContrasenyaAnteriorNoCoincide(EUsuariosWebBase):
    def __init__(self, login):
        EUsuariosWebBase.__init__(self)
        self.login = login
        
    def __str__(self):
        return 'La contraseña anterior del usuario "%s" no coincide' % self.login
