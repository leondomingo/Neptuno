# -*- coding: utf-8 -*-

import cherrypy
import simplejson
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.neptunofactory import get_claseusuarios
from libpy.util import EFaltaParametro
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.clases')
from nucleo.const_datos import ROL_CLASES
from libpy.roles import RolClases
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
Usuarios.privl_clases = RolClases(ROL_CLASES)

class ClasesNoPermitidas(NeptunoBase):
    
    @cherrypy.expose
    def default(self, **params):
        try:
            conector = Conexion()
            usuario = self.check_session(conector, Usuarios, **params)

            return simplejson.dumps(usuario.getListaClasesProhibidas())
            
        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)