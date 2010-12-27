# -*- coding: utf-8 -*-

from mod_python import apache
from nucleo.config import VARIABLES, IMPLEMENTATION_TYPE
from libpy.conexion import Conexion
from libpy.excepciones.usuarios import NoExisteUsuario
from libpy.excepciones.eneptuno import SesionIncorrecta
from libpy.util import get_param, EFaltaParametro
from libpy.log import NeptunoLogger
logger = NeptunoLogger.get_logger('sw.variablesSW')
from libpy.neptunofactory import get_claseusuarios
Usuarios = get_claseusuarios(IMPLEMENTATION_TYPE)

def getvariable(req):
    
    try:
        id_usuario = get_param(req.form, 'id_usuario', int)
        id_sesion = get_param(req.form, 'id_sesion', str)
        variable = get_param(req.form, 'variable', str)
        
        conector = Conexion()    
        Usuarios.comprobar_sesion(conector, id_usuario, id_sesion)
    
        valor = VARIABLES.get(variable)
        req.write('%s = "%s"' % (variable, valor))
        
    except (EFaltaParametro, NoExisteUsuario, SesionIncorrecta), e:
        logger.error(e)
        raise apache.SERVER_RETURN, apache.HTTP_FORBIDDEN        
