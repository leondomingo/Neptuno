# -*- coding: utf-8 -*-

class ELoginNeptuno(Exception):
    def __init__(self):
        Exception.__init__(self)
        
class ELoginIncorrecto(ELoginNeptuno):
    def __init__(self, usuario):
        ELoginNeptuno.__init__(self)
        self.usuario = usuario
        
    def __str__(self):
        return 'Login incorrecto para el usuario "%s"' % self.usuario
        
class EGenerandoSesion(ELoginNeptuno):
    def __init__(self):
        ELoginNeptuno.__init__(self)
        
    def __str__(self):
        return 'Error generando sesión'
        
class EContrasenaIncorrecta(ELoginNeptuno):
    def __init__(self):
        ELoginNeptuno.__init__(self)
        
    def __str__(self):
        return 'Contraseña incorrecta'
        
class EGenerandoSalt(ELoginNeptuno):
    def __init__(self):
        ELoginNeptuno.__init__(self)
        
    def __str__(self):
        return 'Error generando el salt'