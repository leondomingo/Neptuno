# -*- coding: utf-8 -*-

from libpy.neptunofactory import get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import get_paramw, EFaltaParametro
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.acciones')
import cherrypy
import simplejson
from libpy.roles import RolAcciones
from nucleo.const_datos import ROL_ACCIONES
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
Usuarios.privl_accion = RolAcciones(ROL_ACCIONES)

class AccionesNoPermitidas(NeptunoBase):
    
    @cherrypy.expose
    def default(self, **params):
        
        try:
            conector = Conexion()
            usuario = self.check_session(conector, Usuarios, **params)

            tabla = get_paramw(params, 'tabla', str)
        
            return simplejson.dumps(usuario.getListaAccionesProhibidas(tabla))

        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)