# -*- coding: utf-8 -*-

from mod_python import apache
from libpy.excepciones.eneptuno import NoTienePrivilegios, \
    NoTienePrivilegiosEscritura, SesionIncorrecta
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.postgres.borrar import delete
from sqlalchemy.exc import IntegrityError
from libpy.const_error import ERROR_DE_INTEGRIDAD
import re
import simplejson
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.util import get_param, EFaltaParametro
from libpy.neptunofactory import get_claseusuarios
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.borrar')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

def index(req):
    """
    IN
      id_usuario  <int>
      id_sesion   <str>
      id          <int>
      tabla       <str>
      
    OUT
      ???
    """

    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion() 
        usr = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
        
        id_registro = get_param(req.form, 'id', int)        
        tabla = get_param(req.form, 'tabla', str)
        
        logger.debug('Usuario "%s" borrando registro "%d" de la tabla "%s"' % \
                        (usr.nombre_usuario, id_registro, tabla))
        
        delete(id_usuario, tabla, id_registro, conector=conector)
        return simplejson.dumps({})
                    
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta, 
            NoTienePrivilegiosEscritura, NoTienePrivilegios), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
    
    except IntegrityError, e:
        mensaje = e.message[e.message.find('DETAIL:'):].replace('DETAIL:', '').strip()
        
        m = re.search('«[a-zA-Z0-9_]*»', mensaje)        
        if m != None:
            excepcion = dict(codigo=ERROR_DE_INTEGRIDAD,
                             texto=m.group().replace('»', '').replace('«', ''))
        else:
            excepcion = dict(codigo=ERROR_DE_INTEGRIDAD, texto=e.message)
            
        return simplejson.dumps(excepcion)