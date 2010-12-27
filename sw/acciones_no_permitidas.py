# -*- coding: utf-8 -*-

from libpy.neptunofactory import get_claseusuarios
from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.util import get_param, EFaltaParametro
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from mod_python import apache
import simplejson
from libpy.roles import RolAcciones
from nucleo.const_datos import ROL_ACCIONES
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
Usuarios.privl_accion = RolAcciones(ROL_ACCIONES)
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.acciones_no_permitidas')

def index(req):
    """
    IN
      id_usuario  <int>
      id_sesion   <str>
      tabla       <str>
      
    OUT
      <list>
    """
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()
        usuario = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
        
        tabla = get_param(req.form, 'tabla', str)

        return simplejson.dumps(usuario.getListaAccionesProhibidas(tabla))
    
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
                
