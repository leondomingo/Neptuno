# -*- coding: utf-8 -*-

import cherrypy
from nucleo.config import VARIABLES, IMPLEMENTATION_TYPE
from libpy.conexion import Conexion
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import get_paramw, EFaltaParametro
from libpy.neptunofactory import get_claseusuarios
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.variables')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

class Variables(NeptunoBase):
    
    def getvariable(self, **params):
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)

            variable = get_paramw(params, 'variable', str)       
        
            valor = VARIABLES.get(variable)
            return '%s = "%s"' % (variable, valor)
            
        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)        
