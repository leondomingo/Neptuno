# -*- coding: utf-8 -*-

from libpy.conexion import Conexion
from nucleo.config import IMPLEMENTATION_TYPE
from libpy.neptunofactory import get_claseusuarios
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import EFaltaParametro, get_param
import simplejson
from mod_python import apache
from nucleo.const_datos import ROL_CLASES
from libpy.roles import RolClases
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)
Usuarios.privl_clases = RolClases(ROL_CLASES)

def index(req):
    """
    IN
      id_usuario  <int>
      id_sesion   <str>
      
    OUT
      []
    """
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        
        conector = Conexion()            
        usuario = Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
        return simplejson.dumps(usuario.getListaClasesProhibidas())
        
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta):
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN
                        
