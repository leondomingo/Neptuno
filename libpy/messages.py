# -*- coding: utf-8 -*-

import const_datos_neptuno as const

def message(func):
    def _message(_self):
        mensaje = func(_self).get(_self.idioma, None)
        if mensaje:
            return mensaje.encode('utf-8')
        
        else:
            return func(_self).get(1).encode('utf-8')
    
    return _message

class MessagesNeptuno(object):
    
    def __init__(self, idioma=const.LANG_ESP):
        self.idioma = idioma
        
    @message
    def getSesionIncorrecta(self):
        return {const.LANG_ESP: u'Sesión incorrecta',
                const.LANG_ENG: u'Incorrect session'}
    
    @message
    def getNoExisteUsuario(self):
        return {const.LANG_ESP: u'El usuario no existe',
                const.LANG_ENG: u'The user does not exist'}
        
    @message
    def getLoginIncorrecto(self):
        return {const.LANG_ESP: u'Login incorrecto',
                const.LANG_ENG: u'Incorrect login'}
        
    @message
    def getErrorGeneral(self):
        return {const.LANG_ESP: u'Ha ocurrido un error',
                const.LANG_ENG: u'An error has occurred',}        