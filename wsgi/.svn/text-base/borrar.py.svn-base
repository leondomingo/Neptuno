#-*- coding: utf-8 -*-

import cherrypy
import re
import simplejson
from libpy.excepciones.eneptuno import NoTienePrivilegios, \
    NoTienePrivilegiosEscritura, SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.postgres.borrar import delete
from sqlalchemy.exc import IntegrityError
from libpy.const_error import ERROR_DE_INTEGRIDAD
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.util import EFaltaParametro, get_paramw
from libpy.log import NeptunoLogger
from wsgi.base import NeptunoBase
logger = NeptunoLogger.get_logger('wsgi.borrar')
from libpy.neptunofactory import get_claseusuarios
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

class Borrar(NeptunoBase):

    @cherrypy.expose
    def default(self, **params):
        """
        IN
          id_usuario  <int>
          id_sesion   <str>
          id          <int>
          tabla       <str>
          
        OUT
          ???
          
        EXC
          FORBIDDEN
        """
        
        try:
            conector = Conexion()
            self.check_session(conector, Usuarios, **params)
            
            id_usuario = get_paramw(params, 'id_usuario', int)

            id_registro = get_paramw(params, 'id', int)        
            tabla = get_paramw(params, 'tabla', str)

            # borrar registro
            delete(id_usuario, tabla, id_registro, conector=conector)
            return simplejson.dumps({})
                        
        except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta, 
                NoTienePrivilegiosEscritura, NoTienePrivilegios), e:
            logger.error(e)
            # FORBIDDEN
            raise cherrypy.HTTPError(403)
        
        except IntegrityError, e:
            logger.error(e)
            mensaje = e.message[e.message.find('DETAIL:'):].replace('DETAIL:', '').strip()
            
            m = re.search('«[a-zA-Z0-9_]*»', mensaje)        
            if m != None:
                excepcion = dict(codigo=ERROR_DE_INTEGRIDAD,
                                 texto=m.group().replace('»', '').replace('«', ''))
            else:
                excepcion = dict(codigo=ERROR_DE_INTEGRIDAD, texto=e.message)
                
            return simplejson.dumps(excepcion)