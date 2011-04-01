# -*- coding: utf-8 -*-

class ENeptunoBase(Exception):
    def __init__(self, usuario, tabla):
        Exception.__init__(self)
        self.usuario = usuario
        self.tabla = tabla

class NoTienePrivilegios(ENeptunoBase):
    
    def __init__(self, usuario, tabla):
        ENeptunoBase.__init__(self, usuario, tabla)
        
    def __str__(self):
        return '"%s": No tiene privilegios para abrir la tabla "%s"' % (self.usuario, self.tabla)
    
class NoTienePrivilegiosEscritura(ENeptunoBase):
    
    def __init__(self, usuario, tabla):
        ENeptunoBase.__init__(self, usuario, tabla)
        
    def __str__(self):
        return '"%s": No tiene privilegios para actualizar la tabla "%s"' % (self.usuario, self.tabla)    

class SesionIncorrecta(Exception):
    def __init__(self):
        Exception.__init__(self)
        
    def __str__(self):
        return 'Sesión incorrecta'
    
class FaltaParametro(Exception):
    def __init__(self, parametro):
        Exception.__init__(self)
        self.parametro = parametro
    
    def __str__(self):
        return 'Falta el parámetro "%s"' % self.parametro
    
class NoExisteFicheroDeConfiguracion(Exception):
    def __init__(self, nombre_fichero):
        Exception.__init__(self)
        self.nombre_fichero = nombre_fichero
        
    def __str__(self):
        return 'No existe fichero de configuración "%s"' % self.nombre_fichero
    
class ENoExisteRegistro(Exception):
    def __init__(self, id):
        Exception.__init__(self)
        self.id = id
        
    def __repr__(self):
        return 'No existe el regsitro %d' % self.id
    
        