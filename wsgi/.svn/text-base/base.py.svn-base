# -*- coding: utf-8 -*-

from libpy.util import get_paramw
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('wsgi.base.NeptunoBase')

class NeptunoBase(object):
    
    def check_session(self, conector, Usuarios, **params):
        
        id_usuario = get_paramw(params, 'id_usuario', int)
        id_sesion = get_paramw(params, 'id_sesion', str)
        
        logger.debug('Comprobando usuario/sesión (%d/%s)' % \
                        (id_usuario, id_sesion))

        return Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)