# -*- coding: utf-8 -*-

from mod_python import apache
from libpy.neptunofactory import load_module, get_claseusuarios
from libpy.conexion import Conexion
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.util import get_param, EFaltaParametro
import simplejson
from nucleo.config import IMPLEMENTATION_TYPE
fs = load_module(IMPLEMENTATION_TYPE, 'fusionar', 'merge')
merge = fs.merge
from libpy.excepciones.eneptuno import ENoExisteRegistro, SesionIncorrecta
from libpy.excepciones.eneptuno import NoTienePrivilegiosEscritura
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.fusionarSW')
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

def index(req):
    """
    Nombre:
        fusionarSW.py
    
    Descripción:
        Fusiona dos registros de una tabla 'nombre_tabla', borrando uno de ellos al final del proceso.

    IN
      nombre_tabla: Nombre de la tabla a la que pertenecen los registros (alumnos, clientes, etc)
      id_destino: Identificador del registro "destino" donde se copiarán todos los datos.
      id_origen: Identificador del registro "origen" desde donde se copiarán todos los datos.            
      id_usuario: Id de usuario
      id_sesion: Id de sesión.
        
    OUT
      Un json de la forma :
      {
       'id_destino': <int>,
       'id_origen': <int>,
       'num_campos': <int>
      }
        
    EXC
      HTTP_FORBIDDEN
    """
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)

        conector = Conexion()
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
        
        nombre_tabla = get_param(req.form, 'nombre_tabla', str)
        id_destino = get_param(req.form, 'id_destino', int)
        id_origen = get_param(req.form, 'id_origen', int)
        
        mezcla = merge(nombre_tabla, id_destino, otros_ids=[id_origen],
                       conector=conector)
        
        return simplejson.dumps(mezcla)
        
    except (EFaltaParametro, SesionIncorrecta, NoExisteUsuario, ENoExisteRegistro, 
            NoTienePrivilegiosEscritura), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
