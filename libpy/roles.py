# -*- coding: utf-8 -*-

from const_datos_neptuno import PRIVL_LECTURA_ESCRITURA
from libpy.excepciones.usuarios import NoExisteRol

class RolBase(object):
    
    def __init__(self, roles=None):
        self.roles = roles

    def getPrivilegio(self, role, item):
        try:
            if self.roles:
                if self.roles.has_key(role):
                    return self.roles[role][item]
                else:
                    raise NoExisteRol(role)
            else:
                return PRIVL_LECTURA_ESCRITURA
            
        except KeyError:
            return PRIVL_LECTURA_ESCRITURA
        
class RolTablas(RolBase):
    pass
        
class RolColumnas(RolBase):
    
    def getPrivilegio(self, role, tabla, columna):
        try:
            if self.roles:
                if self.roles.has_key(role):
                    return self.roles[role][tabla][columna]
                else:
                    raise NoExisteRol(role)

            else:
                return PRIVL_LECTURA_ESCRITURA

        except KeyError: 
            return PRIVL_LECTURA_ESCRITURA


class RolClases(RolBase):
    
    def getListaClases(self, role):
        try:
            if self.roles:
                if self.roles.has_key(role):                
                    return self.roles[role]
                else:
                    raise NoExisteRol(role)
            else:
                return []
            
        except KeyError:
            return []

class RolAcciones(RolBase):
    
    def getListaAcciones(self, role, tabla):
        try:
            if self.roles:
                if self.roles.has_key(role):                
                    return self.roles[role][tabla]
                else:
                    raise NoExisteRol(role)
                
            else:
                return []
            
        except KeyError:
            return []