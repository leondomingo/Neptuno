# -*- coding: utf-8 -*-

class EUsuariosBase(Exception):
    def __init__(self, usuario):
        Exception.__init__(self)
        self.usuario = usuario
        
class NoExisteUsuario(EUsuariosBase):
    def __init__(self, usuario):
        EUsuariosBase.__init__(self, usuario)
        
    def __str__(self):
        return 'No existe el usuario "%s"' % self.usuario
    
class NoExisteRol(EUsuariosBase):
    def __init__(self, rol):
        EUsuariosBase.__init__(self, '')
        self.rol = rol
        
    def __str__(self):
        return 'No existe el rol "%s"' % self.rol
        
class NombreDeUsuarioYaExiste(EUsuariosBase):
    def __init__(self, usuario):
        EUsuariosBase.__init__(self, usuario)
        
    def __str__(self):
        return 'El nombre de usuario "%s" ya está utilizado' % self.usuario       
        
    
                